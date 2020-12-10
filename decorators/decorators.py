import inspect
from log.utils.utils_log import log as utils_log
from log.server.server_log import log as server_log
from log.client.client_log import log as client_log


def log(side):
    def decorator(func):
        def wrapper(*args, **kwargs):
            # func(*args, **kwargs)
            # print(side)
            if side == "server":
                server_log.info(func.__name__ + " " + inspect.stack()[1][3])
            if side == "client":
                client_log.info(func.__name__ + " " + inspect.stack()[1][3])
            else:
                utils_log.info(func.__name__ + " " + inspect.stack()[1][3])
            return func(*args, **kwargs)

        return wrapper

    return decorator
