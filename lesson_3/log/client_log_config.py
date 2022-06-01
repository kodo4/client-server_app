import logging
import os.path

log = logging.getLogger('client')

PATH = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(PATH, 'client.log')
formatter = logging.Formatter("%(asctime)s %(levelname)-8s %(module)-10s"
                              " %(message)s")

file_hand = logging.FileHandler(PATH, encoding='utf-8')

file_hand.setFormatter(formatter)

log.addHandler(file_hand)
log.setLevel(logging.DEBUG)

if __name__ == '__main__':
    log.debug('Отладочная информация')
    log.info('Информация')
    log.warning('Предупреждение')
    log.error('Ошибка')
    log.critical('Критическая ошибка')
