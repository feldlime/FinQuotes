from environs import Env
from datetime import datetime

from gunicorn.glogging import Logger

env = Env()

# The number of pending connections. This refers to the number of clients
# that can be waiting to be served. Exceeding this number results
# in the client getting an error when attempting to connect.
backlog = env.int('GUNICORN_BACKLOG', 2048)


def default_bind() -> str:
    port = env.str('PORT', '5000')
    return f'0.0.0.0:{port}'

# The socket to bind.
bind = env.str('GUNICORN_BIND', default_bind())

# Check the configuration.
check_config = env.bool('GUNICORN_CHECK_CONFIG', False)

# The number of worker processes that this server
# should keep alive for handling requests.
workers = env.int('GUNICORN_WORKERS', 2)

# If a worker does not notify the master process in this
# number of seconds it is killed and a new worker
# is spawned to replace it.
timeout = env.int('GUNICORN_TIMEOUT', 10)

# Timeout for graceful workers restart.
# After receiving a restart signal, workers have this much time to finish
# serving requests. Workers still alive after the timeout (starting
# from the receipt of the restart signal) are force killed.
graceful_timeout = env.int('GUNICORN_GRACEFUL_TIMEOUT', 5)

# The number of seconds to wait for the next
# request on a Keep-Alive HTTP connection.
keepalive = env.int('GUNICORN_KEEPALIVE', 5)    # five seconds

# The path to a log file to write to.
# A path string. "-" means log to stdout.
logfile = env.str('GUNICORN_LOGFILE', '-')

# The granularity of log output.
loglevel = env.str('GUNICORN_LOGLEVEL', 'debug')

# The Error log file to write to.
errorlog = env.str('GUNICORN_ERRORLOG', '-')

# The Access log file to write to.
accesslog = env.str('GUNICORN_ACCESSLOG', '-')

# The access log format.
access_log_format = 'time="%(t)s" ' \
                    'level="DEBUG" ' \
                    'logger="gunicorn.access" ' \
                    'referer="%(f)s" ' \
                    'user_agent="%(a)s" ' \
                    'protocol="%(H)s" ' \
                    'http_method="%(m)s" ' \
                    'url_path="%(U)s" ' \
                    'response_code="%(s)s" ' \
                    'request_time="%(L)s"'


class GunicornLogger(Logger):
    error_fmt = r'time="%(asctime)s" ' \
                r'level="%(levelname)s" ' \
                r'logger="%(name)s" ' \
                r'message="%(message)s" ' \
                r'pid="%(process)d"'

    datefmt = r'%Y-%m-%d %H:%M:%S'

    access_fmt = '%(message)s pid="%(process)d"'

    syslog_fmt = r'time="%(asctime)s" ' \
                 r'level="%(levelname)s" ' \
                 r'logger="%(name)s" ' \
                 r'message="%(message)s" ' \
                 r'pid="%(process)d"'

    def now(self) -> str:
        fmt = '%Y-%m-%d %H:%M:%S'
        return datetime.now().strftime(fmt)


# The logger you want to use to log events in Gunicorn.
#
# The default class (gunicorn.glogging.Logger) handle most of normal
# usages in logging. It provides error and access logging.
logger_class = GunicornLogger
