import os
import pickle
import socket


def send_data(data: dict) -> None:
    """192.168.31.60"""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    receiver_ip = "192.168.31.60"
    receiver_port = 12345
    s.connect((receiver_ip, receiver_port))
    data_bytes = pickle.dumps(data)
    s.sendall(data_bytes)
    s.close()


def accept_data():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("asdasdasdasdasdasdasd--------------------1")
    receiver_ip = "192.168.31.60"
    receiver_port = 12345
    s.bind((receiver_ip, receiver_port))
    print("asdasdasdasdasdasdasd--------------------2")
    s.listen(10)
    print("asdasdasdasdasdasdasd--------------------3")
    connection, address = s.accept()
    print("asdasdasdasdasdasdasd--------------------4")
    data_bytes = b""
    while True:
        chunk = connection.recv(4096)
        if not chunk:
            break
        data_bytes += chunk
    print("asdasdasdasdasdasdasd--------------------5")
    data = pickle.loads(data_bytes)
    print("asdasdasdasdasdasdasd--------------------6")
    print(data)
    connection.close()
    s.close()


accept_data()
