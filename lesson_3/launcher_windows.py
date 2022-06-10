from subprocess import Popen, CREATE_NEW_CONSOLE

clients = []

while True:
    user = input('Запустить сервера (s) / Закрыть сервера (х) /'
                 'Выйти (q): ')
    if user == 'q':
        break
    elif user == 's':
        server = Popen('python server.py', creationflags=CREATE_NEW_CONSOLE)
        for i in range(2):
            clients.append(Popen('python client.py',
                                 creationflags=CREATE_NEW_CONSOLE))

    elif user == 'x':
        server.kill()
        for p in clients:
            p.kill()
