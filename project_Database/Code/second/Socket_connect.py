import pickle
import socket


def send_data(data: dict) -> None:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    receiver_ip = "127.0.0.1"
    receiver_port = 12345
    s.connect((receiver_ip, receiver_port))
    data_bytes = pickle.dumps(data)
    s.sendall(data_bytes)
    s.close()


def accept_data() -> dict:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    receiver_ip = "127.0.0.1"
    receiver_port = 12345
    s.bind((receiver_ip, receiver_port))
    s.listen(10)
    connection, address = s.accept()
    data_bytes = b""
    while True:
        chunk = connection.recv(200)
        if not chunk:
            break
        data_bytes += chunk
    data = pickle.loads(data_bytes)
    return data
    connection.close()
    s.close()
