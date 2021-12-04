import os
from socket import gethostname


IP_SERVER = gethostname()
PORT_SERVER = 3221

DIR = os.path.dirname(os.path.abspath(__file__))
JSON_USER_PATH = f"{DIR}/data/users.json"
JSON_ROOM_PATH = f"{DIR}/data/rooms.json"
TXT_LOGS_PATH = f"{DIR}/data/logs.txt"