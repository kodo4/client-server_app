"""Сервер"""
import select
import socket
import sys
import json
from common.variables import ACTION, ACCOUNT_NAME, RESPONSE, MAX_CONNECTIONS, \
    PRESENCE, TIME, USER, ERROR, DEFAULT_PORT, MESSAGE, MESSAGE_TEXT, SENDER
from common.utils import get_message, send_message
import logging
import log.server_log_config
from decor import log
import time

LOG = logging.getLogger('server')


@log
def process_client_message(message, messages, client):
    """
    Обработчик сообщений от клиентов, принимает словарь -
    сообщение от клиента, проверяет корректность,
    возвращает словать-ответ для клиента
    """
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message \
        and USER in message and message[USER][ACCOUNT_NAME] == 'Guest':
        LOG.info(f'client message is OK')
        send_message(client, {RESPONSE: 200})
        return
    elif ACTION in message and message[ACTION] == MESSAGE and TIME in message \
            and MESSAGE_TEXT in message:
        messages.append((message[USER][ACCOUNT_NAME], message[MESSAGE_TEXT]))
        return
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
    transport.settimeout(1.0)
    LOG.info(f'created socket {transport}')

    clients = []
    messages = []

    # Слушаем порт
    transport.listen(MAX_CONNECTIONS)

    while True:
        try:
            client, client_address = transport.accept()
        except OSError:
            pass
        else:
            LOG.info(f"Получен запрос на соединение от {client_address}")
            clients.append(client)
        finally:
            r_clients = []
            s_clients = []
            try:
                if clients:
                    r_clients, s_clients, err = select.select(clients,
                                                              clients, [], 0)
            except OSError:
                pass

            for r_client in r_clients:
                try:
                    process_client_message(get_message(r_client),
                                           messages, r_client)
                except:
                    LOG.info('При получении сообщения Клиент {} {} отключился'
                             .format(r_client.fileno(),
                                     r_client.getpeername()))
                    r_client.close()
                    clients.remove(r_client)
                    LOG.info('client socket close')
        if messages:
            message = {
                ACTION: MESSAGE,
                SENDER: messages[0][0],
                TIME: time.time(),
                MESSAGE_TEXT: messages[0][1]
            }
            del messages[0]
            for s_client in s_clients:
                try:
                    send_message(s_client, message)
                except:
                    LOG.info('При отправке сообщения Клиент {} {} отключился'
                             .format(s_client.fileno(),
                                     s_client.getpeername()))
                    s_client.close()
                    clients.remove(s_client)


if __name__ == '__main__':
    main()
