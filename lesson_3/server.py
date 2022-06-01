"""Сервер"""

import socket
import sys
import json
from common.variables import ACTION, ACCOUNT_NAME, RESPONSE, MAX_CONNECTIONS, \
    PRESENCE, TIME, USER, ERROR, DEFAULT_PORT
from common.utils import get_message, send_message
import logging
import log.server_log_config
from decor import log

LOG = logging.getLogger('server')


@log
def process_client_message(message):
    """
    Обработчик сообщений от клиентов, принимает словарь -
    сообщение от клиента, проверяет корректность,
    возвращает словать-ответ для клиента
    """
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message \
        and USER in message and message[USER][ACCOUNT_NAME] == 'Guest':
        LOG.info(f'client message is OK')
        return {RESPONSE: 200}
    LOG.warning('Client message is bad.')
    return {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }


def main():
    """
    Загрузка параметров командной строки, если нет параметров,
    то задаём значеня по умолчанию.
    Сначала обрабатываем порт:
    server.py -p 8888 -a 127.0.0.1
    """

    try:
        if '-p' in sys.argv:
            listen_port = int(sys.argv[sys.argv.index('-p') + 1])
            LOG.info(f'PORT - {listen_port}')
        else:
            listen_port = DEFAULT_PORT
            LOG.warning(f'PORT not selected. Used default PORT {DEFAULT_PORT}')
        if listen_port < 1024 or listen_port > 65535:
            raise ValueError
    except IndexError:
        LOG.critical('The -"p" option must be followed by a port number.')
        sys.exit(1)
    except ValueError:
        LOG.critical('The port number can only be specified in the range of '
                     '1024 to 65535')
        sys.exit(1)

    # Затем загружаем какой адрес слушать

    try:
        if '-a' in sys.argv:
            listen_address = sys.argv[sys.argv.index('-a') + 1]
            LOG.info(f'IP - {listen_address}')

        else:
            listen_address = ''
            LOG.warning('IP not selected.')

    except IndexError:

        LOG.critical('After the parameter "-a" - you must specify the address,'
                     'which will listen to the server')
        sys.exit(1)

    # Готовим сокет

    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    transport.bind((listen_address, listen_port))
    LOG.info(f'created socket {transport}')

    # Слушаем порт
    transport.listen(MAX_CONNECTIONS)

    while True:
        client, client_address = transport.accept()
        try:
            message_from_client = get_message(client)
            LOG.info(f'get message from client {message_from_client}')
            response = process_client_message(message_from_client)
            LOG.info(f'ready message to client: {response}')
            send_message(client, response)
            LOG.info(f'send to {client}')
            client.close()
            LOG.info('client socket close')
        except (ValueError, json.JSONDecodeError):
            LOG.critical('Accepted incorrect message from the client.')
            client.close()
            LOG.info('client socket close')


if __name__ == '__main__':
    main()
