class DataBase:
    users: dict[str, str] = {}
    power: dict[str, int] = {}

    def register(self, username: str, password: str) -> None:
        self.users[username] = password
        self.power[username] = 0

    def find(self, username: str) -> str:
        if username in self.users.keys():
            return self.users[username]
        return "wrong"

    def judge_password(self, username: str, password: str) -> bool:
        if username in self.users.keys():
            if password == self.users[username]:
                return True
        return False

    def judge_user(self, username: str) -> bool:
        if username in self.users.keys():
            return True
        return False

    def clean(self) -> None:
        self.power.clear()
        self.users.clear()
