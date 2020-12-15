from sqlalchemy import *
from sqlalchemy.orm import *
import hashlib
from datetime import datetime
from common.setting import TYPE_DB, SERVER_DB_LOCATION


class ServerDB:
    class User:
        def __init__(self, login, password, info):
            self.login = login
            self.password = password
            self.info = info

    class LoginHistory:
        def __init__(self, login):
            self.login = login
            self.time = datetime.now()

    def __init__(self, location=""):
        if location != "":
            self.ENGINE = create_engine(TYPE_DB + location, echo=False, pool_recycle=7200)
        else:
            self.ENGINE = create_engine(TYPE_DB + SERVER_DB_LOCATION, echo=False, pool_recycle=7200)
        self.METADATA = MetaData()

        user_table = Table('user', self.METADATA,
                           Column('id', Integer, primary_key=True, unique=True, autoincrement=True),
                           Column('login', String),
                           Column("password", String),
                           Column('info', String)
                           )

        login_history_table = Table('log_history', self.METADATA,
                                    Column('id', Integer, autoincrement=True, unique=True, primary_key=True),
                                    Column("login", String),
                                    Column("time", String)
                                    )

        # создаем таблицы (как миграции в django ORM)
        self.METADATA.create_all(self.ENGINE)

        # создае связь между классами и таблицами БД
        mapper(self.User, user_table)
        mapper(self.LoginHistory, login_history_table)

        # сессия
        s = sessionmaker(bind=self.ENGINE)
        self.session = s()
        self.session.commit()

    def create_user(self, login, password, about):
        new_user = self.User(login, password, about)
        self.session.add(new_user)
        self.session.commit()

    def get_user_list(self):
        query = self.session.query(
            self.User.id,
            self.User.login,
            self.User.info
        )
        return query.all()

    def get_users_full_info(self):
        query = self.session.query(
            self.User.id,
            self.User.login,
            self.User.password,
            self.User.info
        )
        return query.all()

    def get_user_history(self):
        query = self.session.query(
            self.LoginHistory.id,
            self.LoginHistory.login,
            self.LoginHistory.time
        )
        return query.all()

    def create_login_history(self, login):
        log = self.LoginHistory(login)
        self.session.add(log)
        self.session.commit()


# добавть функции основные операций

if __name__ == '__main__':
    db = ServerDB()


    for i in range(4):
        h = hashlib.md5()
        h.update(b'123456')
        db.create_user(f"user{i}", h.hexdigest(), f"about me {i}")
    # print(db.get_user_history())

    # log = db.LoginHistory("user1")
    # db.session.add(log)
    # db.session.commit()

    # query = db.session.query(
    #    db.User.id,
    #    db.User.login,
    #    db.User.info
    # )

    # print(query.all())

    # db.create_user("user2", "asdf")

    # user = db.User("user3", "about user 3")
    # db.session.add(user)
    # db.session.commit()
