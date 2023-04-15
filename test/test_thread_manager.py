import logging

import requests

from test.test_base import TestBase
from thread_manager import ThreadManager, ThreadArgument, using_thread


class TestThreadManager(TestBase):
    default_arguments = [
        ThreadArgument(thread_name=f"[THREAD-{x}]", args=(f"Thread-{x}", x))
        for x in range(1, 23)
    ]

    def test_print_something(self):
        # given function
        def print_something(name: str, number: int):
            print(name, number)

        # when
        thread_manager = ThreadManager(print_something, self.default_arguments)
        thread_manager.set_concurrency(15)
        thread_manager.run()
        # then
        assert not thread_manager.has_error()

    def test_if_exceed_concurrency_than_arguments_size(self):
        # given function
        def print_something(name: str, number: int):
            print(name, number)

        # when
        thread_manager = ThreadManager(print_something, self.default_arguments)
        thread_manager.set_concurrency(30)
        thread_manager.run()
        # then
        assert not thread_manager.has_error()

    def test_request_get(self):
        # given function
        def request_something(*args, **kwargs):
            request_url = kwargs.get("request_url", "")
            response = requests.get(request_url)
            print(args, response.status_code)

        # when
        thread_manager = ThreadManager(request_something, [
            ThreadArgument(
                thread_name=f"THREAD-{x}",
                args=(f"Thread-{x}",),
                kwargs={"request_url": "https://www.naver.com"}
            ) for x in range(1, 23)
        ])
        thread_manager.run()
        # then
        assert not thread_manager.has_error()

    def test_default_exception_hook(self):
        # given function
        def func_something(*args):
            raise Exception("test_default_exception_hook", args)

        # when
        thread_manager = ThreadManager(func_something, self.default_arguments)
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
            raise Exception("test_default_exception_hook_2", args)

        # when
        thread_manager = ThreadManager(func_something, self.default_arguments)
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
            raise Exception("test error", args)

        custom_errors = []

        def func_exception_hook(*args):
            custom_errors.append(args)

        # when
        thread_manager = ThreadManager(func_something, self.default_arguments, except_hook=func_exception_hook)
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

    def test_logger(self):
        # given
        log = self.get_test_logger("thread.manager")

        # given function
        def print_something(name: str, number: int):
            if number % 3 == 0:
                log.warning(f"{name} {number}")
            else:
                log.info(f"{name} {number}")

        # when
        thread_manager = ThreadManager(print_something, self.default_arguments)
        # then
        thread_manager.run()
        assert not thread_manager.has_error()
        # revert
        log.removeHandler(self.logger_handler)
        log.addHandler(logging.NullHandler())
