from connect.Socket import accept_data
from Middleware.operate import Operator

from Database import Database_table


class MainClass:
    table = Database_table()

    def start(self):
        self.table.extraction()
        accept_data(self.table)

    def close(self):
        self.table.down()


if __name__ == "__main__":
    text = MainClass()
    text.table.extraction()
    database = {}
    database = Operator.analysis("delete from students where id = 3", text.table)
    text.close()
