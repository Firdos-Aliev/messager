import json
import unittest
from common.setting import *
from common.utils import *


class TestSocket:
    """Класс тестов сокета"""

    def get_message(self, message):
        """Тест на получение сообщения и его парсинг по протоколу(не работает по вине программиста)"""
        # message = socket.recv(MAX_PACKAGE_SIZE)  пропускаем эту часть, мы
        # явно передадим то что дает нам сокет
        decoding_message = message.decode(
            ENCODING)  # перевели в utf-8(ENCODING)
        json_message = json.loads(decoding_message)  # из json в python

        if ACTION in json_message:
            if json_message[ACTION] == MESSAGE:
                return protocol_message(json_message)
            if json_message[ACTION] == PRESENCE:
                return protocol_presence(json_message)
        if RESPONSE in json_message:
            return protocol_response(json_message)

        return {RESPONSE: 405}

    def send_message(self, message):
        """Тест отправки сообщения по протоколу"""
        json_message = json.dumps(message)
        encoding_message = json_message.encode(ENCODING)
        return encoding_message
        # socket.send(encoding_message)


class Tests(unittest.TestCase):
    """Класс тестов"""
    socket = TestSocket()

    def test_get_message(self):
        self.assertEqual(self.socket.get_message(
            b'{"action": "presence", "user": "user1"}'),
            {'response': 200})

        self.assertEqual(self.socket.get_message(
            b'{"user": "user1"}'),
            {'response': 405})

    def test_send_message(self):
        self.assertEqual(self.socket.send_message(
            {"action": "presence", "user": "user1"}),
            b'{"action": "presence", "user": "user1"}')


if __name__ == '__main__':
    unittest.main()
