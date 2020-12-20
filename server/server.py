import select
import sys
from socket import socket, AF_INET, SOCK_STREAM, timeout
from common.setting import *
from common import utils
import server_db
from metaclasses.metaclasses import ServerVerifier
from descriptors.descriptors import Port
from sqlalchemy.sql import default_comparator


class Server(metaclass=ServerVerifier):
    """
    Главный класс сервера
    Преднозначеный для приема клиентов и отправки сообщений определенным клиентам,
    так же парсит сообщения и обрабатывает из по протоколу JIM
    Запускаемый на определенном ip (localhost) и любом порте по правилам дескриптора порта
    имеет 2 не обязательных параметра при запуске:
        - порт
        - файл БД сервера
    """
    port = Port()  # дексриптор для порта

    def __init__(self):  # если ввели один параметр, записываем его в порт, иначе порт по умолчанию
        if len(sys.argv) == 2:
            self.port = int(sys.argv[1])
            self.file_db = ""
        elif len(sys.argv) == 3:
            self.port = int(sys.argv[1])
            self.file_db = sys.argv[2]
        else:
            self.port = PORT
            self.file_db = ""

        print(f"Сервер запущен на порте: {self.port}")
        self.server_socket = socket(AF_INET, SOCK_STREAM)  # создаем TCP сокет
        # указываем хост и порт для поключения
        self.server_socket.bind((HOST, self.port))
        # максимальная очередб прослушивания
        self.server_socket.listen(MAX_QUERY_CONNCETIONS)
        # скорость обновления проверки новых запросов
        self.server_socket.settimeout(TIMEOUT)

        self.db = server_db.ServerDB(
            location=self.file_db)  # обьект для работы с БД
        self.client_list = []  # список поключенный пользователей (онлайн)
        self.client_address = {}  # словарь вида имя - сокет
        print("Сервер создан")

    # основная функция сервера, где происходит основной цикл принятия всех
    # сообшений и пользователей
    def run_server(self):
        """Главный цикл сервера, где осуществляется прием всех пользователей"""
        print("Сервер запущен")
        while True:
            try:
                # таймер на ожидание нового подключения задано в timeout
                # серверного сокета
                client_socket, ip_address = self.server_socket.accept()
                # self.server_socket.connect(("localhost", 8000))
                # сохраняем подключенного пользователя
                self.client_list.append(client_socket)
                self.get_user(client_socket)
                print("Новый пользователь подключился успешно")
            except timeout:
                print(
                    "----------------------------------------------------------------------")
                print("Ожидание...")

            r = []  # клиент присылает сообщение
            w = []  # клиент ожидает сообщение
            e = []  # ошибки

            try:
                # селект функция для формирования
                r, w, e = select.select(
                    self.client_list, self.client_list, [], 0)
            except Exception as e:
                print(e)

            # список словарей, где каждый словарь это сообщение
            messages = []

            # принимаем новые сообщения
            messages = self.get_messages(r)
            # отправляем полученные сообщения
            self.send_messages(messages)

    # функция принимает сокет клиента,
    # который только что подключился и добавляет его сокет и имя в словарь
    # всех пользователей
    def get_user(self, client_socket):
        """Функция валидации и приема клиента"""
        message = utils.get_message(client_socket)

        if message[ACTION] == CONNECTION:
            for user in self.db.get_users_full_info():
                if user[1] == message[USER]:
                    if user[2] == message[PASSWORD]:
                        self.client_address[message[USER]] = client_socket
                        utils.send_response(
                            self.client_address[message[USER]], 200)
                        print(f"Пользователь подключился: {message[USER]}")
                        self.db.create_login_history(message[USER])
                        return
                    else:
                        print("Пользователь ввел неверный пароль")
        else:
            self.client_list.remove(client_socket)
        utils.send_response(client_socket, 500)

    # функция приема всех сообщений, принимает список сокетов,
    # которые готовы принять сообщение возвращается список словарей сообщений
    def get_messages(self, clients_socket_to_r):
        """Функция приема всех сообщений, и парсинг по типам запросов на сервер"""
        messages = []
        for i in clients_socket_to_r:
            try:
                message = utils.get_message(i)

                if message[ACTION] == MESSAGE:
                    messages.append(message)
                if message[ACTION] == FRIEND_REQUEST:
                    for user in self.db.get_user_list():
                        if user[1] == message[TO_USER]:
                            msg = {
                                ACTION: FRIEND_REQUEST,
                                ID: user[0],
                                USER: user[1]
                                # можно тут передавать всякого рода информацию
                                # о пользователе
                            }
                            utils.send_message(i, msg)
            except Exception as e:
                print(e)
        return messages

    # функция отправки сообщения конкретным пользователям,
    # принимает список словарей сообщений
    def send_messages(self, messages):
        """Функция отправки всех сообщений"""
        message = {
            ACTION: MESSAGE,
            USER: '',
            TO_USER: '',
            MESSAGE: ''
        }
        for j in range(len(messages)):
            try:
                if messages[j][TO_USER] in self.client_address.keys():
                    message[USER] = messages[j][USER]
                    message[TO_USER] = messages[j][TO_USER]
                    message[MESSAGE] = messages[j][MESSAGE]
                    utils.send_message(
                        self.client_address[messages[j][TO_USER]], message)
                else:
                    print("User is not online")
            except Exception as e:
                print(e)


if __name__ == '__main__':
    # subprocess.Popen('python server.py 7777', creationflags=subprocess.CREATE_NEW_CONSOLE)
    server = Server()
    server.run_server()
