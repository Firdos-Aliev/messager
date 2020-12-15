import sys
import threading
import sqlite3
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout, QScrollArea, QLabel, QPushButton, \
    QTextEdit, QHBoxLayout, QLineEdit, QDialog

from client import User
from common.setting import MESSAGE, USER, ACTION, FRIEND_REQUEST, ID, TO_USER
from common.utils import get_message


class MainForm(QDialog):
    def __init__(self, user_name, password):
        super().__init__()

        self.chat = Chat(self)
        self.chat_with = ""
        self.user_name = user_name
        self.user = User(self.user_name, password)
        self.db = self.user.db

        self.initUI()

    def initUI(self):
        #central_widget = QWidget(self)
        #self.setCentralWidget(central_widget)
        layout = QHBoxLayout()
        self.setLayout(layout)

        self.setGeometry(300, 300, 500, 600)
        self.setWindowTitle(self.user_name)

        user_list = ScrollBarUserList(self)

        self.chat.send_b.clicked.connect(lambda: self.chat.send())

        layout.addWidget(user_list)
        layout.addWidget(self.chat)

        self.show()

        rscv = threading.Thread(target=self.chat.rscv)
        rscv.daemon = True
        rscv.start()


class AuthForm(QMainWindow):
    def __init__(self):
        super().__init__()

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        self.setGeometry(300, 300, 300, 300)
        self.setWindowTitle("Авторизация")

        self.user = None

        login_l = QLabel("логин")
        password_l = QLabel("пароль")

        self.login_field = QLineEdit()
        self.password_field = QLineEdit()

        button = QPushButton("Войти")

        layout.addWidget(login_l)
        layout.addWidget(self.login_field)
        layout.addWidget(password_l)
        layout.addWidget(self.password_field)
        layout.addWidget(button)

        button.clicked.connect(self.auth)

        self.show()

    def auth(self):
        user_name = self.login_field.text()
        password = self.password_field.text()
        self.hide()
        form = MainForm(user_name, password)
        form.exec_()



class Chat(QWidget):
    def __init__(self, main_form):
        super().__init__()

        self.main_form = main_form

        self.setGeometry(300, 300, 300, 300)
        self.setLayout(QVBoxLayout(self))

        self.chat_with = QLabel("Никто не выбран")
        self.text = QTextEdit()
        self.msg_text = QLineEdit()
        self.send_b = QPushButton("Отправить")

        self.layout().addWidget(self.chat_with)
        self.layout().addWidget(self.text)
        self.layout().addWidget(self.msg_text)
        self.layout().addWidget(self.send_b)

        self.show()

    def load_history(self):
        print(self.main_form.db.messaging_history(self.main_form.chat_with))

    def rscv(self):
        while True:
            msg = get_message(self.main_form.user.client)
            print(msg)
            if msg[ACTION] == MESSAGE:
                self.text.insertPlainText(msg[USER] + ": ")
                self.text.insertPlainText(msg[MESSAGE] + "\n")
                self.main_form.db.messaging(msg[USER], msg[TO_USER], msg[MESSAGE])

    def send(self):
        if self.main_form.chat_with == "":
            print("Пользователь не выбран")
        else:
            print(f"User: {self.main_form.user_name}")
            print(f"To_user: {self.main_form.chat_with}")
            print(f"Message: {self.msg_text.text()}")
            self.text.insertPlainText(self.main_form.user_name + ": ")
            self.text.insertPlainText(self.msg_text.text() + "\n")
            self.main_form.user.send_msg(self.main_form.chat_with, self.msg_text.text())


# можно QScrollArea сделать в виже декоратора
class ScrollBarUserList(QWidget):
    def __init__(self, main_form):
        super().__init__()

        self.main_form = main_form

        self.setMaximumWidth(200)
        layout = QVBoxLayout(self)

        scroll = QScrollArea()
        layout.addWidget(scroll)

        self.user_list = UserList(self.main_form)

        scroll.setWidget(self.user_list)

        user_name_line = QLineEdit()
        add_b = QPushButton("Добавить контакт")

        add_b.clicked.connect(lambda: self.add_user(user_name_line.text()))

        layout.addWidget(user_name_line)
        layout.addWidget(add_b)

        self.show()

    def add_user(self, user_name):
        self.user_list.add_user(user_name)


class UserList(QWidget):
    def __init__(self, main_form):
        super().__init__()
        self.main_form = main_form
        self.layout = QVBoxLayout()
        for i in main_form.db.user_list():
            self.layout.addWidget(UserItem(i[1].__str__(), self.main_form))
        self.setLayout(self.layout)

    def add_user(self, user_name):
        self.main_form.db.add_user(user_name)
        self.layout.addWidget(UserItem(user_name, self.main_form))


class UserItem(QWidget):
    def __init__(self, name, main_form):
        super().__init__()

        self.name = name
        self.main_form = main_form

        self.setMinimumSize(100, 70)

        self.layout = QVBoxLayout(self)

        label_name = QLabel(self.name)

        self.layout.addWidget(label_name)
        self.setStyleSheet('border-style: solid; border-width: 1px; border-color: black;')

        self.show()

    def mousePressEvent(self, event):
        self.main_form.chat_with = self.name
        self.main_form.chat.chat_with.setText(self.main_form.chat_with)

        # в clientDB изменить для корректного вывода
        # history = self.main_form.db.messaging_history(self.main_form.chat_with)  # беру историю их чата, чтобы отобразить
        # self.main_form.chat.text.clear()
        # for i in history:
        #   self.main_form.chat.text.insertPlainText(f"{i[1]}: {i[3]}\n")
        print(self.name)
        print("___________________________")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = AuthForm()
    sys.exit(app.exec_())
