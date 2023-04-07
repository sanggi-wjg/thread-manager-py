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
            ThreadArgument(thread_name=f"[THREAD-{x}]", args=(f"Thread-{x}", x))
            for x in range(1, 23)
        ]
        # when
        thread_manager = ThreadManager(print_something, thread_arguments)
        thread_manager.set_concurrency(15)
        thread_manager.run()
        # then
        assert not thread_manager.has_error()

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
        # then
        assert not thread_manager.has_error()

    def test_default_exception_hook(self):
        # given function
        def func_something(*args):
            raise Exception("test_default_exception_hook")

        # given
        thread_arguments = [
            ThreadArgument(thread_name=f"[THREAD-{x}]", args=(f"Thread-{x}",))
            for x in range(1, 23)
        ]
        # when
        thread_manager = ThreadManager(func_something, thread_arguments)
        thread_manager.run()
        # then
        errors = thread_manager.get_errors()
        for e in errors:
            print(e)
        assert thread_manager.get_errors()
        assert thread_manager.has_error()
        assert thread_manager.get_error_count() == 22, f"Errors Length: {len(errors)}"

    def test_default_exception_hook_2(self):
        # given function
        def func_something(*args):
            raise Exception("test_default_exception_hook_2")

        # given
        thread_arguments = [
            ThreadArgument(thread_name=f"[THREAD-{x}]", args=(f"Thread-{x}",))
            for x in range(1, 23)
        ]
        # when
        thread_manager = ThreadManager(func_something, thread_arguments)
        thread_manager.run()
        # then
        errors = thread_manager.get_errors()
        for e in errors:
            print(e)
        assert thread_manager.get_errors()
        assert thread_manager.has_error()
        assert thread_manager.get_error_count() == 22, f"Errors Length: {len(errors)}"

    def test_custom_exception_hook(self):
        # given function
        def func_something(*args):
            raise Exception("test error")

        custom_errors = []

        def func_exception_hook(*args):
            custom_errors.append(args)

        # given
        thread_arguments = [
            ThreadArgument(thread_name=f"[THREAD-{x}]", args=(f"Thread-{x}",))
            for x in range(1, 23)
        ]
        # when
        thread_manager = ThreadManager(func_something, thread_arguments, except_hook=func_exception_hook)
        thread_manager.run()
        # then
        for e in custom_errors:
            print(e)
        assert len(custom_errors) == 22, f"Errors Length: {len(custom_errors)}"
        # then
        assert not thread_manager.has_error()

    def test_using_thread_decorator(self):
        # given
        @using_thread
        def print_something(number, **kwargs):
            print(number, kwargs)

        # when
        for i in range(10):
            # then
            print_something(i, name=f"thread-{i}")
