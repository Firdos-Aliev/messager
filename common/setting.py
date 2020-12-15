PORT = 8888  # порт
HOST = "127.0.0.1"  # хост
MAX_QUERY_CONNCETIONS = 5  # максимальная очередь подключения
MAX_PACKAGE_SIZE = 4096  # максимальный размер передаваемого сообщения
ENCODING = 'utf-8'  # кодировка
TIMEOUT = 1  # timeout для сервера (select)

# протокол передачи данных, для словаря json
ACTION = 'action'
TIME = 'time'
USER = 'user'
TO_USER = 'to'
USERNAME = 'username'
SOCKET = "socket"
PASSWORD = "password"

# протокол типов сообщений
PRESENCE = 'presence'
RESPONSE = 'response'
ERROR = 'error'
MESSAGE = 'message'
CONNECTION = 'connection'
BAD_GATE_WAY = 'bad gate way'
FRIEND_REQUEST = "friend_request"
ID = "id"

# настройки БД
TYPE_DB = 'sqlite:///'
SERVER_DB_LOCATION = 'server_data.sqlite'
CLIENT_DB_LOCATION = 'client_data.sqlite'

SECRET_KEY = b"jkelfnbp"
