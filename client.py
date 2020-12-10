import sys
from socket import socket, AF_INET, SOCK_STREAM
import threading
from metaclasses.metaclasses import ClientVerifier
import sqlite3
from client_db import ClientDB

from common.utils import get_message, send_message
from common.setting import *
from descriptors.descriptors import Port


class User(metaclass=ClientVerifier):
    port = Port()

    def __init__(self):
        if len(sys.argv) == 2:
            self.port = int(sys.argv[1])
        else:
            self.port = PORT  # дексриптор для порта

        print(f"Клиент запущен на порте: {self.port}")
        self.client = socket(AF_INET, SOCK_STREAM)  # Создать сокет TCP
        self.client.connect((HOST, self.port))  # Соединиться с сервером

        self.user_name = input("Input user_name: ")

        self.db = None

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
        message = {
            ACTION: CONNECTION,
            USER: self.user_name,
        }
        send_message(self.client, message)
        response = self.get_response()
        if response[RESPONSE] == 200:
            self.db = ClientDB(self.user_name)
            return 0
        else:
            return -1

    def create_message(self, to, text):
        message = {
            ACTION: MESSAGE,
            USER: self.user_name,
            TO_USER: to,
            MESSAGE: text
        }
        send_message(self.client, message)

    def create_friend_message(self, to):
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

    def send_thread(self):
        while True:
            to_user = input("Получатель: ")
            msg = input(">>>")
            self.create_message(to_user, msg)
            self.db.messaging(self.user_name, to_user, msg)

    def recv_thread(self):
        while True:
            message = get_message(self.client)
            if message[ACTION] == FRIEND_REQUEST:
                self.db.add_user(message[ID], message[USER])
                print("У вас новый контакт")
            print(message)


User()
