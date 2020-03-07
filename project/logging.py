import sys
import logging

level = logging.DEBUG

date_format = '%Y-%m-%d %H:%M:%S'
log_format = '[%(asctime)s] %(name)-10s %(levelname)-8s  PID: %(process)d  %(message)s'
formatter = logging.Formatter(log_format, date_format)

handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(formatter)
handler.setLevel(level)

logger = logging.getLogger('fin-quotes')
logger.addHandler(handler)
logger.setLevel(level)
