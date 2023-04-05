from threading import Thread
from typing import Callable


def using_thread(func: Callable):
    def decorator(*args, **kwargs):
        th = Thread(target=func, args=(*args,), kwargs=kwargs)
        th.start()
        return th

    return decorator

