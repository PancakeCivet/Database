import json
import socket

# 定义服务器地址和端口号
receiver_ip = "127.0.0.1"
receiver_port = 12345

# 创建socket对象
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 连接服务器
s.connect((receiver_ip, receiver_port))

# 发送数据
str_ = """delete from students 
where id = 1"""
s.sendall(str_.encode())

# 接收服务器响应
data = s.recv(1024).decode()
print(data)
data_dict = {}
data_dict = json.loads(data)

# 关闭连接
s.close()
"""
E:/Miniconda/python.exe e:/Code/Database/project_Database/Code_first/Text.py
"""
