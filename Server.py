import socket
from random import randint
from Diffie_Hellman import ProtocolDH


def take_socket(sock: socket.socket, host_number: str, port_number: int) -> None:
    while True:  # попытка занятия порта сервером
        try:
            sock.bind((host_number, port_number))
            print("Используется порт: " + str(port_number))
            break
        except OSError as error:
            print("{} (порт {} занят)".format(error, port_number))
            port_number = randint(1025, 65535)


def check_key(key: int) -> bool:
    with open('Keys', 'r') as file:
        for line in file:
            if int(line) == key:
                return True
    return False


def sender(sock: socket.socket, message: str) -> None:
    sock.send(bytearray(message.encode()))


def reciever(sock: socket.socket) -> str:
    return sock.recv(1024).decode()


SERVER_PUBLIC_KEY = randint(1, 1024)  # создание публичного ключа сервера
SERVER_PRIVATE_KEY = int(open('private_server_key', 'r').read())
HOST = '127.0.0.1'  # номер хоста
PORT = 1025  # номер порта по умолчанию

sock = socket.socket()  # соккет для обмена ключами
message_socket = socket.socket()  # соккет для принятия сообщений от клиента
take_socket(sock, HOST, PORT)  # занятие порта
sock.listen(1)  # прослушивание одного клиента
conn, addr = sock.accept()  # получение номера сокета и адреса клиента
print("Клиент подключился.")
client_public_key = int(reciever(conn))  # получение публичного клиентского ключа от клиента
if check_key(client_public_key):  # проверка ключа на разрешённость
    protocol = ProtocolDH(SERVER_PUBLIC_KEY, client_public_key, SERVER_PRIVATE_KEY)
    sender(conn, str(SERVER_PUBLIC_KEY))  # отправка клиенту свого публичного ключа
    part_key = int(reciever(conn))  # получение частичного ключа от клиента
    sender(conn, str(protocol.get_part_key()))  # отправка клиенту частичного ключа
    protocol.get_ful_key(part_key)  # инициализация полного ключа шифрования для безопасного обмена
    try:
        message_port = int(protocol.decrypt(reciever(conn)))  # получение номера порта для общения
        take_socket(message_socket, HOST, message_port)  # занятие отдельного порта для общение
        message_socket.listen(1)
        conn, addr = message_socket.accept()  # переподключение клиента на новый сокет
        print("Клиент переподключился на указанный соккет.")
        sock.close()  # закрытие соккета для обмена ключами
        while True:
                message = protocol.decrypt(reciever(conn))
                print("Сообщение от клиента:", message)
                if message == 'exit':
                    print("Клиент отключился. Закрытие сервера.")
                    conn.close()
                    break
    except KeyboardInterrupt:
        message_socket.close()
        print("Закрытие сервера.")
    except (OverflowError, ValueError):
        print("Клиент попытался подключиться на несуществующий порт.")
else:  # ключ не проходит проверку, поэтому закрывается соединение для клиента
    print("Получен неверный ключ от клиента. Отключение.")
    conn.close()
