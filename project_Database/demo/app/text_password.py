import sqlite3

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from passlib.context import CryptContext
from pydantic import BaseModel

app = FastAPI()

security = HTTPBasic()
"""HTTPBasic是一个安全类"""
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

"""它提供了密码哈希和验证功能"""


class User(BaseModel):
    username: str
    password: str


class UserInDB(User):
    hashed_password: str


def get_user(username: str):
    conn = sqlite3.connect("users.db")
    """调取数据区的该用户数据"""
    c = conn.cursor()
    c.execute(
        "SELECT username, hashed_password FROM users WHERE username = ?", (username,)
    )
    user = c.fetchone()
    if user:
        return UserInDB(username=user[0], hashed_password=user[1])
    return None


"""该函数时查找数据库中是否有该用户"""


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


"""验证给定的明文密码和哈希密码是否匹配"""


@app.post("/login")
def login(credentials: HTTPBasicCredentials):
    user = get_user(credentials.username)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    if not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return {"message": "Successful login"}


@app.post("/register")
def register(user: User):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    hashed_password = pwd_context.hash(user.password)
    try:
        c.execute("INSERT INTO users VALUES (?, ?)", (user.username, hashed_password))
        conn.commit()
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Username already registered")
    return {"message": "User registered successfully"}


if __name__ == "__main__":
    uvicorn.run(app)
