from datetime import datetime
from sqlalchemy import *
from sqlalchemy.orm import *
from common.setting import TYPE_DB, CLIENT_DB_LOCATION


class ClientDB:
    class User:
        def __init__(self, id, login):
            self.id = id
            self.login = login

    class MessageHistory:
        def __init__(self, user, to_user, message):
            self.id = None
            self.user = user
            self.to = to_user
            self.message = message
            self.time = datetime.now()

    class Friends:
        def __init__(self, id, login):
            self.id = id
            self.login = login

    def __init__(self, user_name):
        self.ENGINE = create_engine(TYPE_DB + user_name + "_" + CLIENT_DB_LOCATION, echo=False, pool_recycle=7200)
        self.METADATA = MetaData()

        user_table = Table("user", self.METADATA,
                           Column('id', Integer, primary_key=True),
                           Column("login", String)
                           )
        message_history = Table("history", self.METADATA,
                                Column('id', Integer, primary_key=True),
                                Column('user', String),
                                Column('to', String),
                                Column("message", Text),
                                Column("time", String)
                                )
        friends = Table("friends", self.METADATA,
                        Column('id', Integer, primary_key=True),
                        Column('login', String)
                        )

        self.METADATA.create_all(self.ENGINE)

        mapper(self.User, user_table)
        mapper(self.MessageHistory, message_history)
        mapper(self.Friends, friends)

        s = sessionmaker(bind=self.ENGINE)
        self.session = s()
        self.session.commit()

    def messaging(self, user, to, msg):
        hist_obj = self.MessageHistory(user, to, msg)
        self.session.add(hist_obj)
        self.session.commit()

    def add_friend(self, id, login):
        new_friend = self.Friends(id, login)
        self.session.add(new_friend)
        self.session.commit()

    def add_user(self, id, login):
        new_user = self.User(id, login)
        self.session.add(new_user)
        self.session.commit()


if __name__ == '__main__':
    pass
    # db = ClientDB("admin_test")
    # db.add_friend(1, "user4")
    # db.add_user(1, "user4")
    # db.messaging("user1", "user2", "hi")
