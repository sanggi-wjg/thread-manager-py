# py-thread-manager
Python Thread Manager

[![✅Build And Test ✅](https://github.com/sanggi-wjg/py-thread-manager/actions/workflows/build-test.yml/badge.svg)](https://github.com/sanggi-wjg/py-thread-manager/actions/workflows/build-test.yml)
[![PyPI version](https://badge.fury.io/py/py-thread-manager.svg)](https://badge.fury.io/py/py-thread-manager)
[![PyPI](https://img.shields.io/pypi/pyversions/py-thread-manager.svg)](https://pypi.python.org/pypi/py-thread-manager)
<br/>
[![CodeFactor](https://www.codefactor.io/repository/github/sanggi-wjg/py-thread-manager/badge)](https://www.codefactor.io/repository/github/sanggi-wjg/py-thread-manager)



## Install
```shell
pip install py-thread-manager
```


## Simple Usage
```python
import time
from thread_manager import ThreadManager, ThreadArgument

def print_something(name: str, number: int):
    print(name, number)
    time.sleep(1)

thread_arguments = [
    ThreadArgument(thread_name=f"[THREAD-{x}]", args=(f"Thread-{x}", x), kwargs={}, )
    for x in range(1, 23)
]
thread_manager = ThreadManager(print_something, thread_arguments)
thread_manager.run()
```


## Simple Usage with Exception Hook
```python
from thread_manager import ThreadManager, ThreadArgument

errors = []

def func_something(*args):
    raise Exception("test error")

def func_exception_hook(*args):
    errors.append(args)

thread_arguments = [
    ThreadArgument(thread_name=f"[THREAD-{x}]", args=(f"Thread-{x}",), kwargs={})
    for x in range(1, 23)
]
thread_manager = ThreadManager(func_something, thread_arguments, except_hook=func_exception_hook)
thread_manager.run()
```