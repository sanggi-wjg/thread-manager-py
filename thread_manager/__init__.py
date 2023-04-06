import logging

from thread_manager.argument import ThreadArgument
from thread_manager.manager import ThreadManager
from thread_manager.decorator import using_thread

logger = logging.getLogger("thread.manager.py")
logger.addHandler(logging.NullHandler())
logger.propagate = False
