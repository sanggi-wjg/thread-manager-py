import time
import unittest

import requests as requests

from thread_manager import ThreadManager, ThreadArgument


class TestPackage(unittest.TestCase):

    def test_print_something(self):
        # given function
        def print_something(name: str, number: int):
            print(name, number)
            time.sleep(1)

        # given
        thread_arguments = [
            ThreadArgument(thread_name=f"[THREAD-{x}]", args=(f"Thread-{x}", x), kwargs={}, )
            for x in range(1, 23)
        ]
        # when
        thread_manager = ThreadManager(print_something, thread_arguments)
        thread_manager.set_concurrency(15)
        thread_manager.run()

    def test_request_get(self):
        # given function
        def request_something(*args, **kwargs):
            response = requests.get(kwargs.get("request_url"))
            print(args, response.status_code)

        # given
        thread_arguments = [
            ThreadArgument(thread_name=f"[THREAD-{x}]", args=(f"Thread-{x}",), kwargs={"request_url": "https://www.naver.com"})
            for x in range(1, 23)
        ]
        # when
        thread_manager = ThreadManager(request_something, thread_arguments)
        thread_manager.run()

    def test_exception_hook(self):
        # given function
        def func_something(*args):
            raise Exception("test error")

        errors = []

        def func_exception_hook(*args):
            errors.append(args)

        # given
        thread_arguments = [
            ThreadArgument(thread_name=f"[THREAD-{x}]", args=(f"Thread-{x}",), kwargs={})
            for x in range(1, 23)
        ]
        # when
        thread_manager = ThreadManager(func_something, thread_arguments, except_hook=func_exception_hook)
        thread_manager.run()
        # then
        assert len(errors) == 22, f"error length: {len(errors)}"
