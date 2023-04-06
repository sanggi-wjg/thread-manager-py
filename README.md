# thread-manager-py
Python Thread Manager

[![✅Build And Test ✅](https://github.com/sanggi-wjg/py-thread-manager/actions/workflows/build-test.yml/badge.svg)](https://github.com/sanggi-wjg/py-thread-manager/actions/workflows/build-test.yml)
[![PyPI version](https://badge.fury.io/py/thread-manager-py.svg)](https://badge.fury.io/py/thread-manager-py)
[![PyPI](https://img.shields.io/pypi/pyversions/thread-manager-py.svg)](https://pypi.python.org/pypi/thread-manager-py)
<br/>
[![CodeFactor](https://www.codefactor.io/repository/github/sanggi-wjg/py-thread-manager/badge)](https://www.codefactor.io/repository/github/sanggi-wjg/py-thread-manager)



## Install
```shell
pip install thread-manager-py
```

## Usage
### You can find examples in `tests/test_package.py`.


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

## Simple Usage with decorator
```python
from thread_manager import using_thread

@using_thread
def print_something(number, **kwargs):
    print(number, kwargs)

# when
for i in range(10):
    # then
    print_something(i, name=f"thread-{i}")
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