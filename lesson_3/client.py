"""Клиент"""

import sys
import json
import socket
import threading
import time
from common.variables import ACTION, ACCOUNT_NAME, RESPONSE, \
    PRESENCE, TIME, USER, ERROR, DEFAULT_PORT, DEFAULT_IP_ADDRESS, MESSAGE, \
    MESSAGE_TEXT, SEND_TO, SENDER
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
            return message[USER]
        LOG.error(f'get message from server {message}')
        return f'400: {message[ERROR]}'
    LOG.error(f'ValueError - no response from server {message}')
    raise ValueError


@log
def message_from_server(transport, client_name):
    while True:
        answer = get_message(transport)
        if ACTION in answer and answer[ACTION] == MESSAGE and \
                client_name == answer[SEND_TO]:
            print(f'\n Вам Пришло сообщение от {answer[SENDER]}:',
                  '\n', answer[MESSAGE_TEXT])


@log
def send_to_server(transport, client_name):
    while True:
        send_to = input('Кому отправить сообщение: ')
        sms = input('Введите сообщение: ')
        msg = {
            ACTION: MESSAGE,
            TIME: time.time(),
            SENDER: client_name,
            SEND_TO: send_to,
            MESSAGE_TEXT: sms
        }
        send_message(transport, msg)


def main():
    """
    Загружаем параметры командной строки
    """
    client_name = input("Введите ваше имя: ")

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
    message_to_server = create_presence(client_name)
    send_message(transport, message_to_server)

    LOG.info('message send')
    try:
        answer = process_ans(get_message(transport))
        print('Hello, ', answer)
        LOG.info(f'get answer from server {answer}')
    except (ValueError, json.JSONDecodeError):
        LOG.error('Failed to decode server message.')

    recieve = threading.Thread(target=message_from_server, args=(transport,
                                                                 client_name))
    recieve.daemon = True
    recieve.start()

    sender = threading.Thread(target=send_to_server, args=(transport,
                                                           client_name))
    sender.daemon = True
    sender.start()

    while True:
        time.sleep(1)
        if recieve.is_alive() and sender.is_alive():
            continue
        break

if __name__ == '__main__':
    main()
