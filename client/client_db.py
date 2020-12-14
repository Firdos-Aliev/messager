from datetime import datetime
from sqlalchemy import *
from sqlalchemy.orm import *
from common.setting import TYPE_DB, CLIENT_DB_LOCATION


class ClientDB:
    class User:
        def __init__(self, login):
            self.login = login

    class MessageHistory:
        def __init__(self, user, to_user, message):
            self.user = user
            self.to = to_user
            self.message = message
            self.time = datetime.now()

    class Friends:
        def __init__(self, login):
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

    def user_list(self):
        query = self.session.query(
            self.User.id,
            self.User.login
        )
        return query.all()

    def messaging_history(self, to_user):
        query = self.session.query(
            self.MessageHistory.id,
            self.MessageHistory.user,
            self.MessageHistory.to,
            self.MessageHistory.message,
            self.MessageHistory.time
        )
        return query.filter_by(user=to_user).all()

    def messaging(self, user, to, msg):
        hist_obj = self.MessageHistory(user, to, msg)
        self.session.add(hist_obj)
        self.session.commit()

    def add_friend(self, login):
        new_friend = self.Friends(login)
        self.session.add(new_friend)
        self.session.commit()

    def add_user(self, login):
        new_user = self.User(login)
        self.session.add(new_user)
        self.session.commit()


if __name__ == '__main__':
    db = ClientDB("user1")
    print(db.messaging_history("user1"))
    # db.add_user("user1")
    # db.add_user("user2")
    # db.add_user("user3")