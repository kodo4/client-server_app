from subprocess import Popen, CREATE_NEW_CONSOLE

recv_list = []
send_list = []
server = []

while True:
    user = input('Запустить сервера (s) / Закрыть сервера (х) /'
                 'Выйти (q): ')
    if user == 'q':
        break
    elif user == 's':
        # server.append(Popen('server.py', creationflags=CREATE_NEW_CONSOLE))
        for _ in range(2):
            recv_list.append(Popen('python recv_client.py', creationflags=
                                   CREATE_NEW_CONSOLE))
            send_list.append(Popen('python send_client.py', creationflags=
                                   CREATE_NEW_CONSOLE))
    elif user == 'x':
        for p in recv_list:
            p.kill()
        for i in send_list:
            i.kill()
        recv_list.clear()
        send_list.clear()
