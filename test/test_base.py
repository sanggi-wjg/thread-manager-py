import logging
import os
import unittest


class TestBase(unittest.TestCase):
    allowed_logger_names = ["thread.manager", "pool.manager"]
    logger_handler = None

    @classmethod
    def _calculate(cls, x):
        assert isinstance(x, int)

        print(f"[{os.getpid()}]  func: {x}\t\t", r := x ** 5 ** 2, flush=True)
        return r

    @classmethod
    def setUpClass(cls):
        # https://docs.python.org/ko/3/library/logging.html#logrecord-attributes
        handler = logging.StreamHandler()
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(asctime)s (%(name)s) (%(levelname)s) [pid:%(process)d] [thread:%(thread)d:%(threadName)s] (%(filename)s L%(lineno)d) %(message)s")
        handler.setFormatter(formatter)
        cls.logger_handler = handler

    def get_test_logger(self, logger_name: str = "thread.manager"):
        assert logger_name in self.allowed_logger_names

        log = logging.getLogger(logger_name)
        log.setLevel(logging.DEBUG)
        log.addHandler(self.logger_handler)
        return log
