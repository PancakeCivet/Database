import socket

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from Socket.socket_send import (
    get_client,
    get_seller,
    juage_seller,
    judge_client,
    register_client,
    register_seller,
    start,
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class User(BaseModel):
    username: str
    """用户名称"""
    password: str
    """用户登录密码"""
    usertype: int
    """"""
    """用户权限，分为0 - 商家，1 - 用户"""
    ban: bool
    """用户是否被封禁"""
    account: str
    """用户登录账户"""
    money: float
    """用户金额"""


class user_register(BaseModel):
    username: str
    password: str
    usertype: int
    account: str


class User_login(BaseModel):
    account: str
    password: str
    usertype: bool


@app.post("/login")
async def login(user: User_login):
    account = user.account
    password = user.password
    usertype = user.usertype
    if usertype == 1:
        message = get_seller(account, password)
    else:
        message = get_client(account, password)
    if message == {}:
        return 1
    if message["ban"] == True:
        return 2
    return 3 + usertype


@app.post("/register")
async def register(user: User):
    username = user.username
    password = user.password
    usertype = user.usertype
    account = user.account
    if usertype == 1:
        if judge_client(account) == True:
            register_client(username, password, usertype, False, account, 0)
            return True
        return False
    else:
        if juage_seller(account) == False:
            register_seller(username, password, usertype, False, account, 0)
            return True
        return False


if __name__ == "__main__":
    receiver_ip = "127.0.0.1"
    receiver_port = 12345
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((receiver_ip, receiver_port))
    start()

"""
E:/Miniconda/python.exe e:/Code/Database/project_Database/code_secode/app/main.py
"""
