import json

from common.setting import *
from decorators.decorators import log


@log("utils")
def get_message(socket):
    message = socket.recv(MAX_PACKAGE_SIZE)  # приняли собщение
    decoding_message = message.decode(ENCODING)  # перевели в utf-8(ENCODING)
    json_message = json.loads(decoding_message)  # из json в python
    return json_message


@log("utils")
def send_message(socket, message):
    json_message = json.dumps(message)
    encoding_message = json_message.encode(ENCODING)
    socket.send(encoding_message)


@log("utils")
def send_response(socket, code):
    response = {RESPONSE: code}
    json_message = json.dumps(response)
    encoding_message = json_message.encode(ENCODING)
    socket.send(encoding_message)


@log("utils")
def protocol_presence(message):
    if USER in message:
        # log.info("protocol_presence")
        return {RESPONSE: 200}
    else:
        # log.error("protocol_presence")
        return {RESPONSE: 406}


@log("utils")
def protocol_message(message):
    if USER in message:
        if TO_USER in message:
            if MESSAGE in message:
                # log.info("protocol_message")
                return {RESPONSE: 200}
            else:
                # log.error("protocol_message")
                return {RESPONSE: 403}
        else:
            # log.error("protocol_message")
            return {RESPONSE: 402}
    else:
        # log.error("protocol_message")
        return {RESPONSE: 401}


@log("utils")
def protocol_response(message):
    if RESPONSE in message:
        # log.info("protocol_response")
        return message
    else:
        # log.error("protocol_response")
        return {RESPONSE: 404}
