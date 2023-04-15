import collections
import logging
import multiprocessing
from multiprocessing import Pool
from multiprocessing.pool import MapResult, IMapIterator
from queue import PriorityQueue
from typing import Callable, Any

log = logging.getLogger("pool.manager")


class PoolManager:
    default_timeout = 30

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(PoolManager, cls).__new__(cls)
        return cls.instance

    def __init__(self, process_count: int = multiprocessing.cpu_count()):
        """
        Constructor
        :param process_count: number of cpu processor, can not exceed than multiprocessing.cpu_count()
        :type process_count: int
        """
        self.task_queue: PriorityQueue = PriorityQueue()
        self.task_result_queue: collections.deque = collections.deque()
        self.pool: Pool = Pool(min(process_count, multiprocessing.cpu_count()))
        log.debug(f"pool manager inited, {min(process_count, multiprocessing.cpu_count())}")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def is_empty_task(self) -> bool:
        return self.task_queue.empty()

    def has_task(self) -> bool:
        return not self.task_queue.empty()

    def clear_task(self) -> bool:
        while self.has_task():
            self.task_queue.get(False)
        log.debug("task_queue cleared")
        return True

    def close(self):
        self.clear_task()
        self.pool.close()

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
        log.debug(f"task_queue put, {priority}, {callable_func}. {arguments}")

    def _get_task(self) -> Callable:
        return self.task_queue.get()

    def add_task_result(self, task_result: Any):
        if isinstance(task_result, list):
            self.task_result_queue.append(task_result)

        elif isinstance(task_result, MapResult):
            self.task_result_queue.append(task_result.get())

        elif isinstance(task_result, IMapIterator):
            self.task_result_queue.append([r for r in task_result])

        else:
            log.warning("task_results not saved.")
            # assert False, "task_results not saved."

    def get_task_result(self) -> collections.deque:
        return self.task_result_queue.copy()

    def _run(self, pool_func: Callable):
        while not self.is_empty_task():
            _, func, arguments = self._get_task()
            result = pool_func(func, arguments)
            log.debug(f"task_queue run, {func}")
            self.add_task_result(result)

    def run_map(self):
        """
        https://stackoverflow.com/questions/26520781/multiprocessing-pool-whats-the-difference-between-map-async-and-imap
        """
        self._run(self.pool.map)

    def run_map_async(self):
        """

        """
        self._run(self.pool.map_async)

    def run_imap(self):
        """

        """
        self._run(self.pool.imap)
