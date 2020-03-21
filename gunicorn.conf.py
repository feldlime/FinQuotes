from multiprocessing import cpu_count

from project import env, settings

with env.prefixed("GUNICORN_"):

    # The number of pending connections.
    backlog = env.int("BACKLOG", 2048)

    # The socket to bind.
    bind = env.str("BIND", settings.BIND)

    # Check the configuration.
    check_config = env.bool("CHECK_CONFIG", False)

    # The number of worker processes that server
    # should keep alive for handling requests.
    workers = env.int("WORKERS", cpu_count() * 2 + 1)

    # The type of workers to use.
    worker_class = env.str("WORKER_CLASS", "aiohttp.GunicornWebWorker")

    # The maximum number of requests a worker will process before restarting.
    # Any value greater than zero will limit the number of requests
    # a work will process before automatically restarting.
    max_requests = env.int("MAX_REQUESTS", 100)

    # If a worker does not notify the master process in this number of
    # seconds it is killed and a new worker is spawned to replace it.
    timeout = env.int("TIMEOUT", 60)

    # Timeout for graceful workers restart.
    #
    # After receiving a restart signal, workers have this much
    # time to finish serving requests. Workers still
    # alive after the timeout are force killed.
    graceful_timeout = env.int("GRACEFUL_TIMEOUT", 5)

    # The number of seconds to wait for the next
    # request on a Keep-Alive HTTP connection.
    keepalive = env.int("KEEPALIVE", 5)

    # Install a trace function that spews every line of Python
    # that is executed when running the server.
    # This is the nuclear option.
    spew = env.bool("SPEW", False)

    # Detach the main Gunicorn process from the controlling
    # terminal with a standard fork sequence.
    daemon = env.bool("DAEMON", False)

    # The path to a log file to write to, default is stdout.
    logfile = env.str("LOGFILE", "-")

    # The granularity of log output.
    loglevel = env.str("LOGLEVEL", "info")

    # The Error log file to write to.
    errorlog = env.str("ERRORLOG", "-")

    # The Access log file to write to.
    accesslog = env.str("ACCESSLOG", "-")
