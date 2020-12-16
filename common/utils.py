import json

from common.setting import *
from Crypto.Cipher import DES
from decorators.decorators import log


def fit8(message):
    if len(message) % 8 != 0:
        space_len = 8 - (len(message) % 8)
        message = message + b" " * space_len
    return message


def encrypt_message(message):
    """Функция шифрации сообщения"""
    message = fit8(message)
    encryptor = DES.new(SECRET_KEY, DES.MODE_ECB)
    return encryptor.encrypt(message)


def decrypt_message(message):
    """Функция дешифрации сообщения"""
    decrypter = DES.new(SECRET_KEY, DES.MODE_ECB)
    return decrypter.decrypt(message)


@log("utils")
def get_message(socket):
    """Функция приема сообщения"""
    message = socket.recv(MAX_PACKAGE_SIZE)  # приняли собщение
    decrypt = decrypt_message(message)
    decoding_message = decrypt.decode(ENCODING)  # перевели в utf-8(ENCODING)
    json_message = json.loads(decoding_message)  # из json в python
    return json_message


@log("utils")
def send_message(socket, message):
    """Функция отправки сообщения"""
    json_message = json.dumps(message)
    encoding_message = json_message.encode(ENCODING)
    encrypt = encrypt_message(encoding_message)
    socket.send(encrypt)


@log("utils")
def send_response(socket, code):
    """Функция отправки ответа"""
    response = {RESPONSE: code}
    json_message = json.dumps(response)
    encoding_message = json_message.encode(ENCODING)
    encrypt = encrypt_message(encoding_message)
    socket.send(encrypt)
