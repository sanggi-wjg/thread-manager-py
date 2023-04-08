import collections
import multiprocessing
from multiprocessing import Pool
from queue import PriorityQueue
from typing import Callable, Any


class PoolManager:
    _instance = None
    default_timeout = 30

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls._instance = super(PoolManager, cls).__new__(cls)
        return cls._instance

    def __init__(self, process_count: int = multiprocessing.cpu_count()):
        """
        Constructor
        :param process_count: number of cpu processor, can not exceed than multiprocessing.cpu_count()
        :type process_count: int
        """
        self.task_queue: PriorityQueue = PriorityQueue()
        self.task_result_queue: collections.deque = collections.deque()
        self.pool: Pool = Pool(min(process_count, multiprocessing.cpu_count()))

    def is_empty_task(self) -> bool:
        return self.task_queue.empty()

    def has_task(self) -> bool:
        return not self.task_queue.empty()

    def clear_task(self) -> bool:
        while self.has_task():
            self.task_queue.get(False)
        return True

    def add_task(self, callable_func: Callable, *arguments: list, priority: int = 100):
        """

        :param callable_func: task function
        :type callable_func: Callable
        :param arguments: func arguments
        :type arguments: list
        :param priority: task priority
        :type priority: int
        """
        self.task_queue.put((priority, callable_func, *arguments), timeout=self.default_timeout)

    def _get_task(self) -> Callable:
        return self.task_queue.get()

    def add_task_result(self, task_result: Any):
        self.task_result_queue.append(task_result)

    def get_task_result(self) -> collections.deque:
        return self.task_result_queue.copy()

    def run_map(self):
        """
        https://stackoverflow.com/questions/26520781/multiprocessing-pool-whats-the-difference-between-map-async-and-imap
        """
        while not self.is_empty_task():
            _, func, arguments = self._get_task()
            result = self.pool.map(func, arguments)
            self.add_task_result(result)

    def run_map_async(self):
        """

        """
        while not self.is_empty_task():
            _, func, arguments = self._get_task()
            result = self.pool.map_async(func, arguments)
            self.add_task_result(result.get())

    def run_imap(self):
        """

        """
        while not self.is_empty_task():
            _, func, arguments = self._get_task()
            result = self.pool.imap(func, arguments)
            self.add_task_result([r for r in result])
