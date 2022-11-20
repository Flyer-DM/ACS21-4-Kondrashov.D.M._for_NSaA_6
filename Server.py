import socket
from random import randint
from Diffie_Hellman import ProtocolDH


def sender(sock: socket.socket, message: str) -> None:
    sock.send(bytearray(message.encode()))


def reciever(sock: socket.socket) -> str:
    return sock.recv(1024).decode()


SERVER_PUBLIC_KEY = randint(1, 1024)  # создание публичного ключа сервера
SERVER_PRIVATE_KEY = randint(1, 1024)  # создание приватного ключа сервера
HOST = '127.0.0.1'  # номер хоста
PORT = 1025  # номер порта по умолчанию

sock = socket.socket()  # создание сокета
while True:  # попытка занятия порта сервера
    try:
        sock.bind((HOST, PORT))
        print("Используется порт: " + str(PORT))
        break
    except OSError as error:
        print("{} (порт {} занят)".format(error, PORT))
        average_port = randint(1025, 65535)
sock.listen(1)  # прослушивание одного клиента
conn, addr = sock.accept()  # получение номера сокета и адреса клиента
client_public_key = int(reciever(conn))  # получение публичного клиентского ключа от клиента
protocol = ProtocolDH(SERVER_PUBLIC_KEY, client_public_key, SERVER_PRIVATE_KEY)
sender(conn, str(SERVER_PUBLIC_KEY))  # отправка клиенту свого публичного ключа
part_key = int(reciever(conn))  # получение частичного ключа от клиента
sender(conn, str(protocol.get_part_key()))  # отправка клиенту частичного ключа
protocol.get_ful_key(part_key)  # инициализация полного ключа шифрования для безопасного обмена
while True:
        message = protocol.decrypt(reciever(conn))
        print("Сообщение от клиента:", message)
        if message == 'exit':
            print("Клиент отключился. Закрытие сервера.")
            conn.close()
            break
