import uvicorn
from database import DataBase
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

data = DataBase()

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class User(BaseModel):
    username: str
    password: str


@app.post("/login")
async def login(user: User):
    username = user.username
    password = user.password
    if data.judge_user(username) == False:
        return 3
    elif (
        data.judge_user(username) == True
        and data.judge_password(username, password) == True
    ):
        data.power[username] = 1
        return 1
    elif (
        data.judge_user(username) == True
        and data.judge_password(username, password) == False
    ):
        return 2


@app.post("/register")
async def register(user: User):
    username = user.username
    password = user.password
    if data.judge_user(username) == False:
        data.register(username, password)
        return True
    return False


if __name__ == "__main__":
    data.clean()
    uvicorn.run(app, port=8080)
