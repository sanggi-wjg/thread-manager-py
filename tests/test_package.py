import unittest

import requests as requests

from thread_manager import ThreadManager, ThreadArgument, using_thread


class TestPackage(unittest.TestCase):

    def test_print_something(self):
        # given function
        def print_something(name: str, number: int):
            print(name, number)

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

    def test_default_exception_hook(self):
        # given function
        def func_something(*args):
            raise Exception("test error")

        # given
        thread_arguments = [
            ThreadArgument(thread_name=f"[THREAD-{x}]", args=(f"Thread-{x}",), kwargs={})
            for x in range(1, 23)
        ]
        # when
        thread_manager = ThreadManager(func_something, thread_arguments)
        thread_manager.run()
        # then
        error_queue = thread_manager.get_error_queue()
        print(error_queue)
        assert len(error_queue) == 22, f"errors length: {len(error_queue)}"

    def test_custom_exception_hook(self):
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
        print(errors)
        assert len(errors) == 22, f"errors length: {len(errors)}"

    def test_using_thread_decorator(self):
        # given
        @using_thread
        def print_something(number, **kwargs):
            print(number, kwargs)

        # when
        for i in range(10):
            # then
            print_something(i, name=f"thread-{i}")
