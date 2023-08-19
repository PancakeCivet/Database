import json
import re
import socket
from pathlib import Path
from typing import Any

from Middleware import Operator

from Database import Database_table, FiledType


def accept_data(database: Database_table) -> None:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    receiver_ip = "127.0.0.1"
    receiver_port = 12345
    s.bind((receiver_ip, receiver_port))
    s.listen(10)
    connection, address = s.accept()
    try:
        while True:
            text = connection.recv(4096).decode()
            result = Operator.analysis(text, database)
            result_text = json.dumps(result)
            connection.send(result_text.encode())
    except OSError as Ose:
        pass
