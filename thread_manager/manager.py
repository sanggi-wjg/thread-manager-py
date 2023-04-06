import collections
import threading
from threading import Thread, RLock
from typing import List, Callable

from .argument import ThreadArgument

_thread_error_queue = collections.deque()


def default_thread_exception_hook(*args):
    _thread_error_queue.append(*args)


class ThreadManager:
    default_thead_manager_concurrency = 10

    def __init__(self, callable_func: Callable, thread_arguments: List[ThreadArgument], except_hook: Callable = default_thread_exception_hook):
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
        self.thread_arguments: List[ThreadArgument] = thread_arguments
        self.total_thread_arguments_count: int = len(thread_arguments)
        self.concurrency: int = self.default_thead_manager_concurrency
        self.threads: List[Thread] = []
        self.is_interrupted: bool = False
        self.consumer_lock = RLock()
        threading.excepthook = except_hook

    def get_error_queue(self) -> collections.deque:
        return _thread_error_queue.copy()

    def set_concurrency(self, number: int):
        """
        동시 실행 수 설정
        :param number: number of concurrency, 동시 실행 수
        :type number: int
        """
        self.concurrency = number

    def stop(self):
        """
        Stop ThreadManager
        """
        self.is_interrupted = True

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
        while True:
            is_exceed_index = start_index >= self.total_thread_arguments_count
            if self.is_interrupted or is_exceed_index:
                return
            # 만약 end_index 가 총 실행 크기 보다 크다면 end_index 를 실행 크기로 맞추어 IndexError 방지
            end_index = start_index + self.concurrency
            if end_index > self.total_thread_arguments_count:
                end_index = self.total_thread_arguments_count

            self.start_thread(start_index, end_index)
            start_index += self.concurrency
