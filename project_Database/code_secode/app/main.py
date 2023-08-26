import socket

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from Socket.socket_send import (
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


@app.post("/login")
async def login(user: User):
    pass


@app.post("/register")
async def register(user: User):
    username = user.username
    password = user.password
    usertype = user.usertype
    ban = user.ban
    account = user.account
    money = user.money
    if usertype == 1:
        if judge_client(account) == True:
            register_client(username, password, usertype, ban, account, money)
            return True
        return False
    else:
        if juage_seller(account) == False:
            register_seller(username, password, usertype, ban, account, money)
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
