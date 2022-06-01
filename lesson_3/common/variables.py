"""Константы"""

# Порт по усолчанию для сетевого взаимодействия
DEFAULT_PORT = 7777
# ip фдрус по умолчанию для подключения клиента
DEFAULT_IP_ADDRESS = '127.0.0.1'
# Максимальая очередь подключений
MAX_CONNECTIONS = 5
# Максимальная длина сообщения в байтах
MAX_PACKAGE_LENGTH = 1024
# Кодировка проекта
ENCODING = 'utf-8'

# Протокол JIM основные ключи
ACTION = 'action'
TIME = 'time'
USER = 'user'
ACCOUNT_NAME = 'account_name'

# Прочие ключи, используемые в протокле
PRESENCE = 'presence'
RESPONSE = 'response'
ERROR = 'error'
