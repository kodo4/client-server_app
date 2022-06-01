import platform
import subprocess
import chardet

PARAM = '-n' if platform.system().lower() == 'windows' else '-c'


def main(site):
    args = ['ping', PARAM, '2', site]
    process = subprocess.Popen(args, stdout=subprocess.PIPE)
    for line in process.stdout:
        result = chardet.detect(line)
        print('result', result)
        line = line.decode(result['encoding']).encode('utf-8')
        print(line.decode('utf-8'))
        print(25 * '-')


main('yandex.ru')
main('google.com')
