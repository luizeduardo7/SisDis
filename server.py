# Implementação baseada no material do campus e utilizando como base o 
# video: https://www.youtube.com/watch?v=slC-qNFm6hg

import threading
import socket

host = '192.168.1.19'
port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
nicknames = []

def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} saiu do chat!'.encode('ascii'))
            nicknames.remove(nickname)
            break

def receive():
    while True:
        client, address = server.accept()
        print(f'Conectado com {str(address)}')

        client.send('NOME'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        print(f'O nome do cliente e {nickname}!')
        broadcast(f'{nickname} entrou no chat!'.encode('ascii'))
        client.send('Conectado no servidor!'.encode('ascii'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print('Servidor está online...')
receive()
