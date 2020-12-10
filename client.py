import sys
from socket import socket, AF_INET, SOCK_STREAM
import threading
from metaclasses.metaclasses import ClientVerifier
import sqlite3
from client_db import ClientDB

from common.utils import get_message, send_message
from common.setting import ACTION, USER, TO_USER, MESSAGE, PRESENCE, HOST, PORT, MAX_PACKAGE_SIZE, ENCODING, CONNECTION, \
    BAD_GATE_WAY
from descriptors.descriptors import Port


# в функции create_connection перейти на клиентсую БД или поменять логику функции(верификация и подключению к серверу)

class User(metaclass=ClientVerifier):
    port = Port()

    def __init__(self, user_name):
        if len(sys.argv) == 2:
            self.port = int(sys.argv[1])
        else:
            self.port = PORT  # дексриптор для порта

        print(f"Клиент запущен на порте: {self.port}")
        self.client = socket(AF_INET, SOCK_STREAM)  # Создать сокет TCP
        self.client.connect((HOST, self.port))  # Соединиться с сервером
        self.db = ClientDB(user_name)
        self.user_name = input("Input user_name: ")

        status = self.create_connection()
        if status == 0:
            read = threading.Thread(target=self.recv_thread)
            read.daemon = True
            read.start()

            write = threading.Thread(target=self.send_thread)
            write.daemon = True
            write.start()

            write.join()
            read.join()

    def create_connection(self):
        connection = sqlite3.connect("server_data.sqlite")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM user;")
        result = cursor.fetchall()
        print(result)
        for i in result:
            if i[1] == self.user_name:
                message = {
                    ACTION: CONNECTION,
                    USER: self.user_name,
                }
                send_message(self.client, message)
                return 0

        print("Вы еще не зарегестрированы")
        message = {
            ACTION: BAD_GATE_WAY,
            USER: self.user_name,
        }
        send_message(self.client, message)
        input('Press Enter to exit...')
        return -1

    def create_message(self, to, text):
        message = {
            ACTION: MESSAGE,
            USER: self.user_name,
            TO_USER: to,
            MESSAGE: text
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

    def send_thread(self):
        while True:
            to_user = input("Получатель: ")
            msg = input(">>>")
            self.create_message(to_user, msg)
            self.db.messaging(self.user_name, to_user, msg)

    def recv_thread(self):
        while True:
            print(get_message(self.client))


User(input("Enter user name: "))
