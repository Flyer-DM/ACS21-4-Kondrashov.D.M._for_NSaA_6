class ProtocolDH:

    def __init__(self, pub_key_1, pub_key_2, pr_key):
        """Инифиализация публичных ключей для обмена и приватного ключа для определённого пользователя"""
        self.__public_key_1 = pub_key_1
        self.__public_key_2 = pub_key_2
        self.__private_key = pr_key
        self.__full_key = None

    def get_part_key(self):
        """Создание частичного ключа для обмена между пользователями"""
        return self.__public_key_1 ** self.__private_key % self.__public_key_2

    def get_ful_key(self, partial_key):
        """Создания полного ключа на основе двух публичных ключей и собственного"""
        full_key = partial_key ** self.__private_key % self.__public_key_2
        self.__full_key = full_key
        return full_key

    def encrypt(self, message: str):
        """Зашифровка сообщения через полный ключ"""
        return ''.join([chr(ord(symbol) + ord(self.__full_key) % 65536) for symbol in message])

    def decrypt(self, message: str):
        """Функция дешифрования сообщения через полный ключ"""
        return ''.join([chr(ord(symbol) - ord(self.__full_key) % 65536) for symbol in message])

