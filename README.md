# thread-manager-py
Python Thread Manager

[![✅Build And Test ✅](https://github.com/sanggi-wjg/py-thread-manager/actions/workflows/build-test.yml/badge.svg)](https://github.com/sanggi-wjg/py-thread-manager/actions/workflows/build-test.yml)
[![PyPI version](https://badge.fury.io/py/thread-manager-py.svg)](https://badge.fury.io/py/thread-manager-py)
[![PyPI](https://img.shields.io/pypi/pyversions/thread-manager-py.svg)](https://pypi.python.org/pypi/thread-manager-py)
<br/>
[![CodeFactor](https://www.codefactor.io/repository/github/sanggi-wjg/thread-manager-py/badge)](https://www.codefactor.io/repository/github/sanggi-wjg/thread-manager-py)



## Install
```shell
pip install thread-manager-py
```


## Pool Manager Usage
#### You can find examples in `tests/test_package.py`.


### Simple Usage
```python
import os
from pool_manager import PoolManager

def _calculate(x):
    print(f"[{os.getpid()}]  func: {x}\t\t", r := x ** 5 ** 2, flush=True)
    return r

manager = PoolManager()
manager.add_task(_calculate, [i for i in range(2, 22)])
manager.run_map()
manager.add_task(_calculate, [i for i in range(2, 22)])
manager.add_task(_calculate, [i for i in range(2, 22)])
manager.run_map()
task_result = manager.get_task_result()
```



## Thread Manager Usage
#### You can find examples in `tests/test_package.py`.


### Simple Usage
```python
import time
from thread_manager import ThreadManager, ThreadArgument

def print_something(name: str, number: int):
    print(name, number)
    time.sleep(1)

thread_manager = ThreadManager(print_something, [
    ThreadArgument(thread_name=f"Thread:{x}", args=(x, x), kwargs={}, ) for x in range(1, 23)
])
thread_manager.run()
```


### Get Thread Error
```python
errors = thread_manager.get_errors()
has_error = thread_manager.has_error()
error_count = thread_manager.get_error_count()

for e in errors:
    print(e)
```


### Simple Usage with decorator
```python
from thread_manager import using_thread

@using_thread
def print_something(number, **kwargs):
    print(number, kwargs)

for i in range(10):
    print_something(i, name=f"thread-{i}")
```


### Simple Usage with Exception Hook
```python
from thread_manager import ThreadManager, ThreadArgument

errors = []

def func_something(*args):
    raise Exception("test error")

def func_exception_hook(*args):
    errors.append(args)

thread_manager = ThreadManager(func_something, [
    ThreadArgument(thread_name=f"Thread:{x}", args=(x, x), kwargs={}, )
    for x in range(1, 23)
], except_hook=func_exception_hook)
thread_manager.run()
```