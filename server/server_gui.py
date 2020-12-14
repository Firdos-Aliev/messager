import subprocess
import sys
from server_db import *
from descriptors.descriptors import Port
from common.setting import PORT

from PyQt5.QtWidgets import QMainWindow, QApplication, QAction, QTableWidget, QVBoxLayout, QWidget, QPushButton, \
    QTableWidgetItem, QToolBar, QLineEdit, QLabel, QFileDialog


class MainForm(QMainWindow):
    def __init__(self, db_file_name=""):
        super().__init__()

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        self.db_file_name = db_file_name
        self.db = ServerDB(location=db_file_name)
        self.setWindowTitle("Администрирование сервера")
        self.setGeometry(300, 300, 600, 300)

        users_table = UsersTable(self)
        users_info = UserInfo(self)
        settings = SettingsWidget(self)

        tools = Tools(users_table, users_info, settings)

        layout.addWidget(tools)
        layout.addWidget(users_table)
        layout.addWidget(users_info)
        layout.addWidget(settings)

        self.show()


class SettingsWidget(QWidget):
    def __init__(self, main_form):
        super().__init__()

        self.active_proc = []

        self.main = main_form

        self.hide()
        self.layout = QVBoxLayout(self)

        self.start_b = QPushButton("start server")
        self.start_b.clicked.connect(self.run_server)

        port_label = QLabel("Port")
        self.port_area = QLineEdit()

        self.db_b = QPushButton("Выбрать файл БД")
        self.db_b.clicked.connect(self.get_file)

        self.layout.addWidget(port_label)
        self.layout.addWidget(self.port_area)
        self.layout.addWidget(self.db_b)
        self.layout.addWidget(self.start_b)

    def get_file(self):
        file = QFileDialog().getOpenFileName(filter="*.sqlite")
        file_dir = file[0].split("/")[-1]
        subprocess.Popen(f'python server_gui.py {file_dir}')
        self.main.close()

    def run_server(self):
        if len(self.active_proc) > 0:
            proc = self.active_proc.pop()
            proc.kill()

        if self.port_area.text() != "":
            port = int(self.port_area.text())
            self.active_proc.append(
                subprocess.Popen(f'python server.py {port} {self.main.db_file_name}',
                                 creationflags=subprocess.CREATE_NEW_CONSOLE))
        else:
            self.active_proc.append(subprocess.Popen(f'python server.py {PORT} {self.main.db_file_name}',
                                                     creationflags=subprocess.CREATE_NEW_CONSOLE))

    def change_status(self):
        if self.isHidden():
            self.show()
        else:
            self.hide()


class Tools(QToolBar):
    def __init__(self, user_table, user_info, settings):
        super().__init__()

        client_list = QAction("клиенты", self)
        client_list.triggered.connect(user_table.change_status)

        client_info = QAction("статистика", self)
        client_info.triggered.connect(user_info.change_status)

        settings_widget = QAction("настройки", self)
        settings_widget.triggered.connect(settings.change_status)

        self.addAction(client_list)
        self.addAction(client_info)
        self.addAction(settings_widget)


class UserInfo(QWidget):
    def __init__(self, main_form):
        super().__init__()

        self.hide()  # скрываем

        self.layout = QVBoxLayout(self)  # ставим layout

        self.main = main_form

        self.table = QTableWidget()  # настраиваем и заполеняем таблицу
        self.table.setColumnCount(3)
        self.table.setRowCount(0)
        self.table.setHorizontalHeaderLabels(["id", "login", "time"])
        self.update_table()

        self.push_info = QPushButton("update")  # добавляем кнопку обновления
        self.push_info.clicked.connect(self.update_table)

        self.layout.addWidget(self.table)  # добавляем еа виджет все элементы
        self.layout.addWidget(self.push_info)

    def update_table(self):
        data = self.main.db.get_user_history()
        self.table.setRowCount(0)  # очищаем таблицу

        for id, login, time in data:  # заполняем таблицу
            row = self.table.rowCount()
            self.table.setRowCount(row + 1)

            self.table.setItem(row, 0, QTableWidgetItem(id.__str__()))
            self.table.setItem(row, 1, QTableWidgetItem(login.__str__()))
            self.table.setItem(row, 2, QTableWidgetItem(time.__str__()))

    def change_status(self):
        if self.isHidden():
            self.show()
        else:
            self.hide()


class UsersTable(QWidget):
    def __init__(self, main_form):
        super().__init__()

        self.layout = QVBoxLayout(self)

        self.hide()

        self.main = main_form

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setRowCount(0)
        self.table.setHorizontalHeaderLabels(["id", "login", "info"])
        self.update_table()

        self.push_user = QPushButton("update")
        self.push_user.clicked.connect(self.update_table)

        self.layout.addWidget(self.table)
        self.layout.addWidget(self.push_user)

    def update_table(self):
        user_list = self.main.db.get_user_list()  # берем из БД данные
        self.table.setRowCount(0)  # очищаем таблицу

        for id, login, info in user_list:  # заполняем таблицу
            row = self.table.rowCount()
            self.table.setRowCount(row + 1)

            self.table.setItem(row, 0, QTableWidgetItem(id.__str__()))
            self.table.setItem(row, 1, QTableWidgetItem(login.__str__()))
            self.table.setItem(row, 2, QTableWidgetItem(info.__str__()))

    def change_status(self):
        if self.isHidden():
            self.show()
        else:
            self.hide()


if __name__ == '__main__':
    if len(sys.argv) > 1:
        file = sys.argv[1]
    else:
        file = ""
    app = QApplication(sys.argv)
    form = MainForm(db_file_name=file)
    sys.exit(app.exec_())
