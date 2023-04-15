import logging

from pool_manager import PoolManager
from test.test_base import TestBase


class TestPollManager(TestBase):
    default_range = [i for i in range(2, 32)]

    def test_task_queue(self):
        # given
        manager = PoolManager(2)
        # when
        manager.add_task(self._calculate, self.default_range)
        # then
        assert not manager.is_empty_task()
        assert manager.has_task()
        assert manager.clear_task()
        manager.run_map()
        manager.close()

    def test_context_manager(self):
        with PoolManager() as manager:
            manager.add_task(self._calculate, self.default_range)
            manager.add_task(self._calculate, self.default_range)
            manager.add_task(self._calculate, self.default_range)
            manager.run_map()
            assert manager.get_task_result()
            assert not manager.has_task()

    def test_run(self):
        # given
        manager = PoolManager()
        # when
        manager.add_task(self._calculate, self.default_range)
        manager.run_map()
        manager.add_task(self._calculate, self.default_range)
        manager.add_task(self._calculate, self.default_range)
        manager.run_map()
        # then
        task_result = manager.get_task_result()
        assert task_result
        manager.close()

    def test_run_async(self):
        # given
        manager = PoolManager()
        # when
        manager.add_task(self._calculate, self.default_range)
        manager.run_map_async()
        manager.add_task(self._calculate, self.default_range)
        manager.add_task(self._calculate, self.default_range)
        manager.run_map_async()
        # then
        task_result = manager.get_task_result()
        assert task_result
        manager.close()

    def test_run_imap(self):
        # given
        manager = PoolManager()
        # when
        manager.add_task(self._calculate, self.default_range)
        manager.run_imap()
        manager.add_task(self._calculate, self.default_range)
        manager.add_task(self._calculate, self.default_range)
        manager.run_imap()
        # then
        task_result = manager.get_task_result()
        assert task_result
        manager.close()

    def test_logger(self):
        log = self.get_test_logger("pool.manager")

        # given
        manager = PoolManager()
        # when
        manager.add_task(self._calculate, self.default_range)
        manager.run_map()
        # then
        task_result = manager.get_task_result()
        assert task_result
        assert not manager.has_task()
        # revert
        log.removeHandler(self.logger_handler)
        log.addHandler(logging.NullHandler())
        manager.close()
