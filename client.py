# Implementação baseada no material do campus e utilizando como base o 
# video: https://www.youtube.com/watch?v=slC-qNFm6hg

import socket
import threading

nickname = input("Escolha um apelido: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('192.168.104.25', 55555))

def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NOME':
                client.send(nickname.encode('ascii'))
            else:
                print(message)
        except:
            print('Um erro ocorreu!')
            client.close()
            break

def write():
    while True:
        message = nickname+": "+input("")
        client.send(message.encode('ascii'))

receiveThread = threading.Thread(target=receive)
receiveThread.start()

writeThread = threading.Thread(target=write)
writeThread.start()
