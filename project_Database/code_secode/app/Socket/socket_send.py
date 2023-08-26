import json
import socket

receiver_ip = "127.0.0.1"
receiver_port = 12345
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((receiver_ip, receiver_port))


def start():
    str_ = """CREATE TABLE goods (name TEXT, price INT, Introduction TEXT);"""
    s.sendall(str_.encode())
    data = s.recv(1024).decode()

    str_ = """CREATE TABLE client (name TEXT, password TEXT, type INT, ban BOOLAN, account TEXT, money FLOAT);"""
    s.sendall(str_.encode())
    data = s.recv(1024).decode()

    str_ = """CREATE TABLE seller (name TEXT, password TEXT, type INT, ban BOOLAN, account TEXT, money FLOAT);"""
    s.sendall(str_.encode())
    data = s.recv(1024).decode()


def register_client(
    username: str, password: str, usertype: int, ban: bool, account: str, money: float
):
    str_ = f"INSERT INTO client VALUES ({username},{password},{usertype},{ban},{account},{money})"
    s.sendall(str_.encode())
    data = s.recv(1024).decode()


def register_seller(
    username: str, password: str, usertype: int, ban: bool, account: str, money: float
):
    str_ = f"INSERT INTO seller VALUES ({username},{password},{usertype},{ban},{account},{money})"
    s.sendall(str_.encode())
    data = s.recv(1024).decode()


def judge_client(account: str) -> bool:
    str_ = f"SELECT account From client"
    s.sendall(str_.encode())
    data = s.recv(1024).decode()
    data = json.loads(data)
    for element in data["filed_row"]:
        if element["account"] == account:
            return False
    return True


def juage_seller(account: str) -> bool:
    str_ = f"SELECT account From seller"
    s.sendall(str_.encode())
    data = s.recv(1024).decode()
    data = json.loads(data)
    for element in data["filed_row"]:
        if element["account"] == account:
            return False
    return True


"""
E:/Miniconda/python.exe e:/Code/Database/project_Database/code_secode/app/socket/socket_send.py
"""
