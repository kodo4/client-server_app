"""Клиент"""

import sys
import json
import socket
import time
from common.variables import ACTION, ACCOUNT_NAME, RESPONSE, \
    PRESENCE, TIME, USER, ERROR, DEFAULT_PORT, DEFAULT_IP_ADDRESS
from common.utils import get_message, send_message
import logging
import log.client_log_config
from decor import log

LOG = logging.getLogger('client')


@log
def create_presence(account_name='Guest'):
    """
    Функция генерирует запрос о присутствии клиента
    """
    out = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name
        }
    }
    LOG.info(f'generate presence message: {out}')
    return out


@log
def process_ans(message):
    """
    Функция разбирает ответ сервера
    """
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            LOG.info(f'get message from server {message}')
            return '200: OK'
        LOG.error(f'get message from server {message}')
        return f'400: {message[ERROR]}'
    LOG.error(f'ValueError - no response from server {message}')
    raise ValueError


def main():
    """
    Загружаем параметры командной строки
    """
    try:
        server_address = sys.argv[1]
        server_port = int(sys.argv[2])
        LOG.info(f'used PORT - {server_port}, IP - {server_address}')
        if server_port < 1024 or server_port > 65535:
            raise ValueError
    except IndexError:
        LOG.warning(f'IP and PORT not selected. Used default IP - '
                    f'{DEFAULT_IP_ADDRESS}, PORT - {DEFAULT_PORT}')
        server_address = DEFAULT_IP_ADDRESS
        server_port = DEFAULT_PORT
    except ValueError:
        LOG.critical(f'port not in 1024 and 65535.')
        sys.exit()

    # Инициализация сокета и обмен

    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    LOG.info(f'create socket {transport}')
    transport.connect((server_address, server_port))
    LOG.info(f'connect to server with IP {server_address} '
             f'PORT - {server_port}')
    message_to_server = create_presence('Guest')
    send_message(transport, message_to_server)
    LOG.info('message send')
    try:
        answer = process_ans(get_message(transport))
        LOG.info(f'get answer from server {answer}')
    except (ValueError, json.JSONDecodeError):
        LOG.error('Failed to decode server message.')


if __name__ == '__main__':
    main()
