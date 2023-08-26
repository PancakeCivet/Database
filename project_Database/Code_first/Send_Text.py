import json
import socket

# 定义服务器地址和端口号
receiver_ip = "127.0.0.1"
receiver_port = 12345
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((receiver_ip, receiver_port))
str_ = """CREATE TABLE goods (name TEXT, price INT, Introduction TEXT);"""
s.sendall(str_.encode())
data = s.recv(1024).decode()
print(data)
data_dict = {}
data_dict = json.loads(data)


str_ = """CREATE TABLE client (name TEXT,password TEXT);"""
s.sendall(str_.encode())
data = s.recv(1024).decode()
print(data)
data_dict = {}
data_dict = json.loads(data)

str_ = """CREATE TABLE seller (name TEXT,password TEXT);"""
s.sendall(str_.encode())
data = s.recv(1024).decode()
print(data)
data_dict = {}
data_dict = json.loads(data)


"""
E:/Miniconda/python.exe e:/Code/Database/project_Database/Code_first/Send_Text.py
"""
