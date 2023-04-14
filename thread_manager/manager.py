import collections
import logging
import threading
from _thread import _ExceptHookArgs as ExceptHookArgs
from threading import Thread, RLock
from typing import List, Callable

from .argument import ThreadArgument

log = logging.getLogger("thread.manager")


class ThreadManager:
    default_concurrency = 10

    def __init__(self, callable_func: Callable, thread_arguments: List[ThreadArgument], except_hook: Callable = None):
        """
        Constructor
        :param callable_func: source function, 실행할 함수
        :type callable_func: Callable
        :param thread_arguments: thread arguments of source function, 실행할 함수의 인자
        :type thread_arguments: List[tuple]
        :param except_hook: when error occurred, run hook function, 에러시 실행할 함수의 인자
        :type except_hook: Callable
        """
        self.func: Callable = callable_func
        # threads
        self.threads: List[Thread] = []
        self.thread_arguments: List[ThreadArgument] = thread_arguments
        self.thread_arguments_count: int = len(thread_arguments)
        # configs
        self.concurrency: int = self.default_concurrency
        self.is_interrupted: bool = False
        self.consumer_lock = RLock()
        # errors
        self.error_deque = collections.deque()
        self.set_exception_hook(self.add_errors if except_hook is None else except_hook)
        log.debug(f"thread manager inited, "
                  f"func: {self.func.__name__}, "
                  f"thread_arguments_count: {self.thread_arguments_count}, "
                  f"except_hook: {'default except_hook' if except_hook is None else except_hook}")

    def set_exception_hook(self, except_hook: Callable):
        threading.excepthook = except_hook

    def add_errors(self, error: ExceptHookArgs):
        self.error_deque.append(error)
        log.debug(f"error appended : {error}")

    def get_errors(self) -> collections.deque:
        return self.error_deque.copy()

    def get_error_count(self) -> int:
        return len(self.error_deque)

    def has_error(self) -> bool:
        return len(self.error_deque) > 0

    def set_concurrency(self, number: int):
        """
        동시 실행 수 설정
        :param number: number of concurrency, 동시 실행 수
        :type number: int
        """
        self.concurrency = number
        log.debug(f"concurrency changed to {number}")

    def stop(self):
        """
        Stop ThreadManager
        """
        self.is_interrupted = True
        log.debug(f"requested to stop")

    def start_thread(self, start: int, end: int):
        """
        Execute Thread
        :param start: index of start
        :type start: int
        :param end: index of end
        :type end: int
        """
        # Thread R-Lock
        with self.consumer_lock:
            # concurrency_limit 개수 만큼 Thread 실행
            for i in range(start, end, self.concurrency):
                self.threads = [
                    Thread(
                        target=self.func,
                        name=argument.thread_name,
                        args=argument.args,
                        kwargs=argument.kwargs,
                    )
                    for argument in self.thread_arguments[i:i + self.concurrency]
                ]
                for th in self.threads:
                    th.start()
                for th in self.threads:
                    th.join()
                del self.threads

    def run(self):
        start_index = 0
        # 중지 상태 혹은 완료 되면 종료
        while not self.is_interrupted and (start_index <= self.thread_arguments_count):
            # 만약 end_index 가 총 실행 크기 보다 크다면 end_index 를 실행 크기로 맞추어 IndexError 방지
            end_index = start_index + self.concurrency
            if end_index > self.thread_arguments_count:
                end_index = self.thread_arguments_count

            self.start_thread(start_index, end_index)
            log.debug(f"{start_index}~{end_index} threads finished")
            start_index += self.concurrency
