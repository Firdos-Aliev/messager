from Crypto.Cipher import DES
import json

from common.setting import SECRET_KEY

key = SECRET_KEY


def fit8(message):
    if len(message) % 8 != 0:
        space_len = 8 - (len(message) % 8)
        message = message + b" " * space_len
    return message


def encrypt_message(message):
    message = fit8(message)
    encryptor = DES.new(key, DES.MODE_ECB)
    return encryptor.encrypt(message)


def decrypt_message(message):
    decrypter = DES.new(key, DES.MODE_ECB)
    return decrypter.decrypt(message)


msg = {
    "action": "message",
    "message": "123"
}
print(msg)  # словарь
json_message = json.dumps(msg)
print(json_message)  # строка (json)
encoding_message = json_message.encode("utf-8")
print(encoding_message)  # байты
encrypt = encrypt_message(encoding_message)
print(type(encrypt))  # закодированое

decrypt = decrypt_message(encrypt)
print(decrypt)
decoding_message = decrypt.decode("utf-8")
print(decrypt)
json_message = json.loads(decoding_message)
print(json_message)