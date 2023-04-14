import logging

from pool_manager.manager import PoolManager

logger = logging.getLogger("pool.manager")
logger.addHandler(logging.NullHandler())
logger.propagate = False
