import sys
import threading

from PyQt5.QtWidgets import QMainWindow, QApplication, QListView, QWidget, QVBoxLayout, QScrollArea, QTableWidget, \
    QTableWidgetItem, QLabel, QPushButton, QTextEdit, QHBoxLayout, QLineEdit
from common.setting import MESSAGE, USER

from client import User
from common.utils import get_message


class MainForm(QMainWindow):
    def __init__(self, user_name):
        super().__init__()

        self.chat_with = ""
        self.user_name = user_name
        self.user = User(self.user_name)
        self.db = self.user.db

        self.initUI()

    def initUI(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QHBoxLayout()
        central_widget.setLayout(layout)

        self.setGeometry(300, 300, 500, 600)
        self.setWindowTitle(self.user_name)

        user_list = ScrollBarUserList(self)
        chat = Chat(self)

        chat.send_b.clicked.connect(lambda: chat.send())

        layout.addWidget(user_list)
        layout.addWidget(chat)

        self.show()

        rscv = threading.Thread(target=chat.rscv)
        rscv.daemon = True
        rscv.start()


class Chat(QWidget):
    def __init__(self, main_form):
        super().__init__()

        self.main_form = main_form

        self.setGeometry(300, 300, 300, 300)
        self.setLayout(QVBoxLayout(self))

        self.text = QTextEdit()
        self.msg_text = QLineEdit()
        self.send_b = QPushButton("Отправить")

        self.layout().addWidget(self.text)
        self.layout().addWidget(self.msg_text)
        self.layout().addWidget(self.send_b)

        self.show()

    # реализовать при помощи сигналов
    def rscv(self):
        while True:
            msg = get_message(self.main_form.user.client)
            self.text.insertPlainText(msg[USER] + ": ")
            self.text.insertPlainText(msg[MESSAGE] + "\n")

    def send(self):
        if self.main_form.chat_with == "":
            print("Пользователь не выбран")
        else:
            print(f"User: {self.main_form.user_name}")
            print(f"To_user: {self.main_form.chat_with}")
            print(f"Message: {self.msg_text.text()}")
            self.main_form.user.send_msg(self.main_form.chat_with, self.msg_text.text())


# можно QScrollArea сделать в виже декоратора
class ScrollBarUserList(QWidget):
    def __init__(self, main_form):
        super().__init__()
        self.setMaximumWidth(200)
        layout = QVBoxLayout(self)

        scroll = QScrollArea()
        layout.addWidget(scroll)

        scroll.setWidget(UserList(main_form))

        add_b = QPushButton("Добавить контакт")

        add_b.clicked.connect(lambda: print(123))

        layout.addWidget(add_b)

        self.show()


class UserList(QWidget):
    def __init__(self, main_form):
        super().__init__()
        layout = QVBoxLayout()
        for i in main_form.db.user_list():
            layout.addWidget(UserItem(i[0].__str__(), i[1].__str__(), main_form))
        self.setLayout(layout)


class UserItem(QWidget):
    def __init__(self, id, name, main_form):
        super().__init__()

        self.id = id
        self.name = name
        self.main_form = main_form

        self.layout = QVBoxLayout(self)

        label_id = QLabel(self.id)
        label_id.hide()
        label_name = QLabel(self.name)

        self.layout.addWidget(label_id)
        self.layout.addWidget(label_name)
        self.show()

    def mousePressEvent(self, event):
        self.main_form.chat_with = self.name
        print(self.id)
        print(self.name)
        print("___________________________")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = MainForm("user1")
    sys.exit(app.exec_())
