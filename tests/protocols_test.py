import unittest
from common.utils import *


class TestProtocol(unittest.TestCase):

    def test_protocol_presence(self):
        self.assertEqual(protocol_presence(
            {'action': 'presence', 'user': 'user2'}),
            {RESPONSE: 200})

    def test_protocol_message(self):
        self.assertEqual(protocol_presence(
            {'action': 'message', 'user': 'user1', 'to': 'user2', 'message': 'hi'}),
            {RESPONSE: 200})

    def test_protocol_response(self):
        self.assertEqual(protocol_response(
            {'response': 200}),
            {'response': 200})


if __name__ == '__main__':
    unittest.main()
