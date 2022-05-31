import logging
import sys
from log import server_log_config, client_log_config


def log(func):
    """Декаратор"""
    def decorator(*args, **kwargs):
        """Обертка"""
        log_name = 'server' if 'server.py' in sys.argv[0] else 'client'
        LOGGER = logging.getLogger(log_name)

        result = func(*args, **kwargs)
        LOGGER.info(f'Функция {func.__name__}, аргументы: {args}, {kwargs}')
        LOGGER.info(f'Функция {func.__name__} была вызвана из функции '
                    f'{func.__module__}')
        return result
    return decorator
