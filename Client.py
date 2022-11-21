import socket
import re
from random import randint
from Diffie_Hellman import ProtocolDH


def sender(sock: socket.socket, message: str) -> None:
    sock.send(bytearray(message.encode()))


def reciever(sock: socket.socket, printable=False) -> str:
    message = sock.recv(1024).decode()
    if printable:
        print("Сообщение от сервера: ", message)
    return message


CLIENT_PRIVATE_KEY = randint(1, 1024)  # создание приватного ключа клиента

sock = socket.socket()
flag = True
try:
    while True:
            ip_add_server = input('Введите IP адрес сервера (имя хоста): ')
            port_server = input('Введите номер порта сервера: ')
            try:
                port_server = int(port_server)
            except ValueError:
                print("Номер порта введён неверно.")
                flag = not flag
                break
            if re.match('^localhost|(((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)(\.(?!$)|$)){4})$', ip_add_server) is None:
                print("Адрес сервера введён неверно.")
                flag = not flag
                break
            if flag:
                print("Подключение к серверу.")
                sock.connect((ip_add_server, port_server))  # имя хоста и номер порта
                client_public_key = int(input("Введите публичный клиентский ключ шифрования: "))
                sender(sock, str(client_public_key))  # отправка публичного ключа клиента серверу
                server_public_key = int(reciever(sock))  # получение публичного ключа сервера
                protocol = ProtocolDH(server_public_key, client_public_key, CLIENT_PRIVATE_KEY)
                sender(sock, str(protocol.get_part_key()))  # отправка частичного ключа серверу
                part_key = int(reciever(sock))  # получение частичного ключа сервера
                protocol.get_ful_key(part_key)  # инициализация полного ключа шифрования для безопасного обмена
                message_port = input("Введите адрес порта для передачи сообщений на сервер: ")
                sender(sock, protocol.encrypt(message_port))
                sock.close()  # закрытие соккета для обмена ключами
                sock = socket.socket()
                sock.connect((ip_add_server, int(message_port)))
                print("Успешное подключение к серверу.")
                while True:
                    message = input(">>")
                    if message == 'exit':
                        sender(sock, protocol.encrypt(message))  # шифрование сообщения от клиента и отключение
                        sock.close()
                        break
                    sender(sock, protocol.encrypt(message))  # шифрование сообщения от клиента
                break
            else:
                break
except ConnectionRefusedError:
    print("Подключение не установлено (возможно, введён неверный номер порта).")
except ValueError:
    print("Подключение не установлено (возможно, публичный ключ клиента не прошёл проверку).")
