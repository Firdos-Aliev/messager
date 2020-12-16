import sys
import hashlib
from socket import socket, AF_INET, SOCK_STREAM
import threading

from metaclasses.metaclasses import ClientVerifier

from client_db import ClientDB

from common.utils import get_message, send_message
from common.setting import *
from descriptors.descriptors import Port


class User(metaclass=ClientVerifier):
    """Главный класс клиента, в нем осуществялется инициализация всех нужных сущностей для работы с сервером"""
    port = Port()

    def __init__(self, user_name, password):
        if len(sys.argv) == 2:
            self.port = int(sys.argv[1])
        else:
            self.port = PORT  # дексриптор для порта

        print(f"Клиент запущен на порте: {self.port}")
        self.client = socket(AF_INET, SOCK_STREAM)  # Создать сокет TCP
        self.client.connect((HOST, self.port))  # Соединиться с сервером

        self.user_name = user_name
        self.hash = hashlib.md5()
        self.db = None

        self.hash.update(password.encode(ENCODING))
        status = self.create_connection(self.hash.hexdigest())
        if status == 0 and __name__ == "__main__":
            read = threading.Thread(target=self.recv_thread)
            read.daemon = True
            read.start()

            write = threading.Thread(target=self.send_thread)
            write.daemon = True
            write.start()

            read.join()
            write.join()

    def create_connection(self, password):
        """Функция валидации и подключения с сервером, также подключение к клиентской БД"""
        message = {
            ACTION: CONNECTION,
            USER: self.user_name,
            PASSWORD: password
        }
        send_message(self.client, message)
        response = self.get_response()
        if response[RESPONSE] == 200:
            self.db = ClientDB(self.user_name)
            return 0
        else:
            return -1

    def create_message(self, to, text):
        """Функция отправки сообщения определенному клиенту"""
        message = {
            ACTION: MESSAGE,
            USER: self.user_name,
            TO_USER: to,
            MESSAGE: text
        }
        send_message(self.client, message)

    def create_friend_message(self, to):
        """Функция на зпрос серверу на добавление в друзья"""
        message = {
            ACTION: FRIEND_REQUEST,
            TO_USER: to
        }
        send_message(self.client, message)

    def create_presence(self):
        message = {
            ACTION: PRESENCE,
            USER: self.user_name,
        }
        send_message(self.client, message)

    def get_response(self):
        return get_message(self.client)

    def send_msg(self, to, msg):
        """Функция отправки сообщения + учет истори исообщений"""
        self.create_message(to, msg)
        self.db.messaging(self.user_name, to, msg)

    def send_thread(self):
        """Поток для отправки сообщений"""
        while True:
            to_user = input("Получатель: ")
            msg = input(">>>")
            self.create_message(to_user, msg)
            self.db.messaging(self.user_name, to_user, msg)

    def recv_thread(self):
        """Потоко на получение всех сообщений"""
        while True:
            message = get_message(self.client)
            if message[ACTION] == FRIEND_REQUEST:
                self.db.add_user(message[USER])
                print("У вас новый контакт")
            print(message)


if __name__ == '__main__':
    User("user2", "123456")
