import logging

from project.logging import handler, level

logger = logging.getLogger('api')
logger.addHandler(handler)
logger.setLevel(level)
