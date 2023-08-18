import json
import os
import pickle
import pprint
import re
import socket
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any

"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """"""

"""
数据库表建立
"""


class FiledType(str, Enum):
    """字段数据类型"""

    INT = "INT"
    FLOAT = "FLOAT"
    TEXT = "TEXT"
    BOOLEAN = "BOOLEAN"
    DATE = "DATE"


class Filed:

    """字段"""

    name: str
    """字段名"""
    type: FiledType
    """字段类型"""

    def __init__(self, name: str, type: FiledType) -> None:
        self.name = name
        self.type = type
        """初始化并赋值"""

    def __repr__(self) -> str:
        return f"{self.name}     {self.type}\n"

    def json(self) -> dict:
        return {"name": self.name, "type": self.type}
        """返回json格式数据"""

    def load(self, data: dict) -> None:
        self.name = data["name"]
        self.type = FiledType(data["type"])
        """加载json格式数据"""


class Table_struct:
    name: str
    """表的名字"""
    filed_column: list[Filed]
    """存储字段列表"""
    filed_row: list[dict[str, Any]]
    """存储字段记录"""

    def __init__(self) -> None:
        self.name = ""
        self.filed_column = []
        self.filed_row = []

    def __repr__(self) -> str:
        return f"{self.filed_column}    {self.filed_row}"

    """初始化"""

    def json(self) -> dict:
        filed_list_temp = []
        for element in self.filed_column:
            filed_list_temp.append(element.json())
        return {
            "name": self.name,
            "filed_column": filed_list_temp,
            "filed_row": self.filed_row,
        }

    """将数据转为JSON格式"""

    def load(self, data: dict) -> None:
        self.name = data["name"]
        for element in data["filed_column"]:
            self.filed_column.append(Filed(element["name"], FiledType(element["type"])))
        self.filed_row = data["filed_row"]

    """将JSON格式转为类"""


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """"""


"""测试函数"""


def Te():
    print(
        "\n\n\n\n\n\n\n--------------------------------------------------------------------------------\n\n\n\n\n\n\n\n"
    )


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """"""

"""
数据库本身
"""

Table_dict: dict[str, Table_struct] = {}
"""建立字典，运用字典的key对应表的name找到表所对应的Table_struct"""


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """"""


"""socket部分"""


def send_data() -> None:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    receiver_ip = "127.0.0.1"
    receiver_port = 12345
    s.connect((receiver_ip, receiver_port))
    SQL = s.recv(2000000)
    SQL_finally = pickle.loads(SQL)
    analysis(SQL_finally)
    data_bytes = pickle.dumps(Table_dict)
    s.sendall(data_bytes)


def accept_data() -> None:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    receiver_ip = "127.0.0.1"
    receiver_port = 12345
    s.bind((receiver_ip, receiver_port))
    s.listen(10)
    connection, address = s.accept()
    while True:
        SQL = Input_SQL()
        SQL_finally = pickle.dumps(SQL)
        connection.send(SQL_finally)
        chunk = connection.recv(2000000)
        Table_dict = pickle.loads(chunk)


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """"""


"""
operate部分
"""


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """"""


"""判断条件的类型"""


def Judge(item: str) -> FiledType:
    if ("false" in item) or ("true" in item):
        return FiledType.BOOLEAN
    elif item.isdigit():
        return FiledType.INT
    elif item.replace(".", "", 1).isdigit():
        return FiledType.FLOAT
    elif (item.replace("-", "", 1)).replace("-", "", 1).isdigit():
        return FiledType.DATE
    else:
        return FiledType.TEXT


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """"""


"""表的创建"""


def add_table(table_name: str, content: list[Filed]) -> None:
    Table_dict[table_name] = Table_struct()
    Table_dict[table_name].name = table_name
    Table_dict[table_name].filed_column = content
    Table_dict[table_name].filed_column.insert(0, Filed("Id", FiledType.INT))


# 通过将"Id"字段插入到filed_column列表的开头，它将被视为主键。

"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """"""


"""增"""


def add_row(table_name: str, content: dict[str, Any]) -> None:
    """传入参数：表名，数据"""
    if table_name in Table_dict:
        Id = len(Table_dict[table_name].filed_row)
        content["Id"] = Id
        Table_dict[table_name].filed_row.append(content)
    else:
        print("Wrong operate!!")


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """"""


"""查"""

"""现在的查只是把数据存在一个dict里面，等学完socket后再进行修改"""


"""全查"""


def Fin_all(table_name: str):
    if table_name in Table_dict:
        table_data = {}
        table_data = Table_dict[table_name].json()
        print(table_data)
    else:
        print("Wrong operate!!")


"""只要部分的字段"""


def Fin_part(table_name: str, column_name: list[str]):
    if table_name in Table_dict:
        table_data = Table_struct()
        table_temp = {}
        table_data.name = table_name
        for element in column_name:
            for i in range(len(Table_dict[table_name].filed_row)):
                table_data.filed_row.append(
                    {element: Table_dict[table_name].filed_row[i][element]}
                )
        for element in column_name:
            for item in Table_dict[table_name].filed_column:
                if element == item.name:
                    table_data.filed_column.append(item)
        table_temp = table_data.json()
    else:
        print("Wrong operate!!")


"""查满足条件的"""


def Fin_condition(
    table_name: str, column_name: list[str], condition: dict[str, Any]
) -> None:
    if table_name in Table_dict:
        table_data = Table_struct()
        table_temp = {}
        table_data.name = table_name
        keys = condition.keys()
        key_list = list(keys)
        key_condition = key_list[0]
        for row in Table_dict[table_name].filed_row:
            if row[key_condition] == condition[key_condition]:
                for element in column_name:
                    table_data.filed_row.append({element: row[element]})
                for element in column_name:
                    for item in Table_dict[table_name].filed_column:
                        if element == item.name:
                            table_data.filed_column.append(item)
        table_temp = table_data.json()
    else:
        print("Wrong operate!!")


def Fin_condition_and(
    table_name: str,
    column_name: list[str],
    conditions: list[dict[str, Any]],
) -> None:
    """condition_names中key与value相同"""
    if table_name in Table_dict:
        table_data = Table_struct()
        table_temp = {}
        table_data.name = table_name
        flag_column = True
        for row in Table_dict[table_name].filed_row:
            """对每个数据枚举"""
            flag = 0
            for column in Table_dict[table_name].filed_column:
                for condition in conditions:
                    if column.name in condition:
                        if row[column.name] == condition[column.name]:
                            flag += 1
            if flag == len(conditions):
                flag_column = 1
                for element in column_name:
                    table_data.filed_row.append({element: row[element]})
                if flag_column:
                    flag_column = False
                    for element in column_name:
                        for item in Table_dict[table_name].filed_column:
                            if element == item.name:
                                table_data.filed_column.append(item)
        table_temp = table_data.json()
    else:
        print("Wrong operate!!")


def Fin_condition_or(
    table_name: str,
    column_name: list[str],
    conditions: list[dict[str, Any]],
) -> None:
    """condition_names中key与value相同"""
    if table_name in Table_dict:
        table_data = Table_struct()
        table_temp = {}
        table_data.name = table_name
        flag_column = True
        for row in Table_dict[table_name].filed_row:
            """对每个数据枚举"""
            flag = 0
            for column in Table_dict[table_name].filed_column:
                for condition in conditions:
                    if column.name in condition:
                        if row[column.name] == condition[column.name]:
                            flag += 1
            if flag > 0:
                for element in column_name:
                    table_data.filed_row.append({element: row[element]})
                if flag_column:
                    flag_column = False
                    for element in column_name:
                        for item in Table_dict[table_name].filed_column:
                            if element == item.name:
                                table_data.filed_column.append(item)
        table_temp = table_data.json()
    else:
        print("Wrong operate!!")


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """"""


"""排序"""


def sql_sort(
    table_name: str, column_name: list[str], column_condition: str, direction: str
):
    if table_name in Table_dict:
        table_data = Table_struct()
        table_temp = {}
        row_data = []
        table_data.name = table_name
        for row in Table_dict[table_name].filed_row:
            row_data.append(row[column_condition])
        combined = list(zip(row_data, Table_dict[table_name].filed_row))
        if direction == "DESC":
            combined.sort(key=lambda x: x[0], reverse=True)
        else:
            combined.sort(key=lambda x: x[0], reverse=False)
        row_data, Table_dict[table_name].filed_row = zip(*combined)
        for row in Table_dict[table_name].filed_row:
            for element in column_name:
                table_data.filed_row.append({element: row[element]})
        for element in column_name:
            for item in Table_dict[table_name].filed_column:
                if element == item.name:
                    table_data.filed_column.append(item)
        table_temp = table_data.json()
    else:
        print("Wrong operate!!")


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """"""


"""改"""


def update(
    table_name: str,
    column_name: str,
    content: FiledType,
    row_column_name: str,
    Update: list[dict[str, Any]],
) -> None:
    """传入的参数：表名，字段名，字段名对应的类型，条件，修改的数据"""
    if table_name in Table_dict:
        element = Table_dict[table_name]
        i = 0
        for row in element.filed_row:
            if column_name in row:
                for last in Table_dict[table_name].filed_column:
                    if (
                        (last.name == column_name)
                        and (content == last.type)
                        and (row_column_name == str(row[column_name]))
                    ):
                        for item in Update:
                            for key, value in item.items():
                                if key in row:
                                    Table_dict[table_name].filed_row[i][key] = value
            i += 1
    else:
        print("Wrong operate!!")


"""UPDATE students SET age = 10, name = 'SSADASD' WHERE Id = 0"""

"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """"""


"""删"""


def delete(
    table_name: str, column_name: str, content: FiledType, condition: str
) -> None:
    """传入的参数：表名，字段名，字段名对应的类型，字段名下数据"""
    if table_name in Table_dict:
        element = Table_dict[table_name]
        for row in element.filed_row:
            if column_name in row and row[column_name] == condition:
                for last in Table_dict[table_name].filed_column:
                    if last.name == column_name and content == last.type:
                        element.filed_row.remove(row)
                        for i in range(len(element.filed_row)):
                            element.filed_row[i]["Id"] = i
    else:
        print("Wrong operate!!")


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """"""


"""将数据库保存为JSON文件"""


def down() -> None:
    current_dir = os.getcwd()
    folder_path = os.path.join(current_dir, "Date")
    os.makedirs(folder_path, exist_ok=True)
    file = os.path.join(folder_path, "database.JSON")
    database_temp = {}
    for table_name, table_struct in Table_dict.items():
        database_temp[table_name] = table_struct.json()
    with open(file, "w", encoding="utf-8") as f:
        json.dump(database_temp, f, ensure_ascii=False)
    Table_dict.clear()


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """"""

"""提取JSON文件"""


def extraction() -> None:
    current_dir = os.getcwd()
    folder_path = os.path.join(current_dir, "Date")
    os.makedirs(folder_path, exist_ok=True)
    file = os.path.join(folder_path, "database.JSON")
    database_temp = {}
    with open(file, "r", encoding="utf-8") as f:
        database_temp = json.load(f)
    for table_name, table_data in database_temp.items():
        table_struct = Table_struct()
        table_struct.load(table_data)
        Table_dict[table_name] = table_struct


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """"""

"""解析SQL语句"""


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """"""


"""加数据部分"""


def SQL_add(SQL: str) -> None:
    pattern = r"INSERT INTO\s+(\w+)\s+VALUES\s+\((.*)\)"
    match = re.search(pattern, SQL, re.IGNORECASE)
    if match:
        table_name = match.group(1)
        values = [value.strip() for value in match.group(2).split(",")]
        data_temp = {}
        temp_tot = 0
        for element in Table_dict[table_name].filed_column:
            if element.name == "Id":
                Id_ = len(Table_dict[table_name].filed_row)
                data_temp["Id"] = Id_
            else:
                data_temp[element.name] = values[temp_tot]
                temp_tot += 1
        add_row(table_name, data_temp)


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """"""


"""删数据部分"""


def SQL_delete(SQL: str) -> None:
    pattern = r"DELETE\s+FROM\s+(\w+)\s+WHERE\s+(.*)"
    match = re.search(pattern, SQL, re.IGNORECASE)
    if match:
        table_name = match.group(1)
        conditions = [value.strip() for value in match.group(2).split("=")]
        conditions[1] = conditions[1].strip("';")
        delete(table_name, conditions[0], Judge(conditions[1]), conditions[1])


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """"""


"""查数据部分"""


def SQL_sekect_all(SQL: str) -> None:
    pattern = r"SELECT\s+\*\s+FROM\s+(\w+)"
    match = re.match(pattern, SQL, re.IGNORECASE)
    if match:
        table_name = match.group(1)
        Fin_all(table_name)


def SQL_sekect_part(SQL: str) -> None:
    pattern = r"SELECT\s+(.+)\s+FROM\s+(\w+)"
    match = re.match(pattern, SQL, re.IGNORECASE)
    if match:
        table_name = match.group(2)
        conditions = [value.strip() for value in match.group(1).split(",")]
        Fin_part(table_name, conditions)


def SQL_sekect_or_part(SQL: str) -> None:
    pattern = r"SELECT\s+(.+)\s+FROM\s+(\w+)\s+WHERE\s+(.+)$"
    match = re.search(pattern, SQL, re.IGNORECASE)

    if match:
        condition_dict: list[dict[str, Any]] = []
        table_name = match.group(2)
        conditions = [value.strip() for value in match.group(3).split("or")]
        columns = [value.strip() for value in match.group(1).split(",")]
        for i in range(len(columns)):
            columns[i] = columns[i].strip("' ")
        for condition in conditions:
            parts = condition.split("=")
            key = parts[0].strip()
            value = parts[1].strip()
            key = key.strip("' ")
            value = value.strip("' ")
            condition_dict.append({key: value})
        Fin_condition_or(table_name, columns, condition_dict)


def SQL_sekect_and_part(SQL: str):
    pattern = r"SELECT\s+(.+)\s+FROM\s+(\w+)\s+WHERE\s+(.+)$"
    match = re.search(pattern, SQL, re.IGNORECASE)

    if match:
        condition_dict: list[dict[str, Any]] = []
        table_name = match.group(2)
        conditions = [value.strip() for value in match.group(3).split("and")]
        columns = [value.strip() for value in match.group(1).split(",")]
        for i in range(len(columns)):
            columns[i] = columns[i].strip("' ")
        for condition in conditions:
            parts = condition.split("=")
            key = parts[0].strip()
            value = parts[1].strip()
            key = key.strip("' ")
            value = value.strip("' ")
            condition_dict.append({key: value})
        Fin_condition_and(table_name, columns, condition_dict)


def SQL_sekect_condition(SQL) -> None:
    pattern = r"SELECT\s+(.+)\s+FROM\s+(\w+)\s+WHERE\s+(.+)$"
    match = re.search(pattern, SQL, re.IGNORECASE)
    if match:
        condition_dict = {}
        table_name = match.group(2)
        columns = [value.strip() for value in match.group(1).split(",")]
        for i in range(len(columns)):
            columns[i] = columns[i].strip("' ")
        condition = [value.strip() for value in match.group(3).split("=")]
        condition[1] = condition[1].strip("';")
        condition_dict[condition[0]] = condition[1]
        Fin_condition(table_name, columns, condition_dict)


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """"""


"""分治"""


def SQL_sekect(SQL: str) -> None:
    if "*" in SQL:
        # print("SQL_sekect_all")
        SQL_sekect_all(SQL)
    elif "where" in SQL:
        if "or" in SQL:
            # print("SQL_sekect_or_part")
            SQL_sekect_or_part(SQL)
        elif "and" in SQL:
            # print("SQL_sekect_and_part")
            SQL_sekect_and_part(SQL)
        else:
            # print("SQL_sekect_condition")
            SQL_sekect_condition(SQL)
    else:
        # print("SQL_sekect_part")
        SQL_sekect_part(SQL)


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """"""


"""改数据部分"""


def SQL_updata(SQL: str) -> None:
    pattern = r"UPDATE\s+(\w+)\s+SET\s+((?:\w+\s*=\s*(?:\w+|'.*?')(?:,\s*\w+\s*=\s*(?:\w+|'.*?'))*))\s+WHERE\s+(.*)"
    match = re.search(pattern, SQL, re.IGNORECASE)
    if match:
        table_name = match.group(1)
        set_clause = [value.strip() for value in match.group(2).split(",")]
        conditions = [value.strip() for value in match.group(3).split("=")]
        for i in range(len(set_clause)):
            set_clause[i] = set_clause[i].strip("' ")
            set_clause[i] = set_clause[i].split("=")
        Updata: list[dict[str, Any]] = []
        conditions[1] = conditions[1].strip("';")
        for i in range(len(set_clause)):
            key = set_clause[i][0]
            value = set_clause[i][1]
            key = key.strip("' ")
            value = value.strip("' ")
            Updata.append({key: value})
        print(Judge(conditions[1]))
        update(
            table_name,
            conditions[0],
            Judge(conditions[1]),
            conditions[1],
            Updata,
        )


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """"""


"""排序部分"""


def SQL_sort(SQL: str) -> None:
    pattern_columns = r"SELECT\s(.*?)\sFROM"
    pattern_order_by = r"ORDER BY\s(.*?)\s(ASC|DESC)"
    pattern_table_name = r"FROM\s+(\w+)\s"
    table_name = re.findall(pattern_table_name, SQL, re.IGNORECASE)
    columns = re.findall(pattern_columns, SQL, re.IGNORECASE)
    order_by = re.findall(pattern_order_by, SQL, re.IGNORECASE)
    for i in range(len(columns)):
        columns[i] = columns[i].split(",")
    for i in range(len(columns[0])):
        columns[0][i] = columns[0][i].strip("' ")
    order_by = [(col.strip(), order.strip()) for col, order in order_by]
    sql_sort(table_name[0], columns[0], order_by[0][0], order_by[0][1])


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """"""


"""分析SQL语句"""


def analysis(SQL: str) -> None:
    sql = SQL.upper()
    if "INSERT INTO" in sql:
        SQL_add(SQL)
        return
    if "DELETE" in sql:
        SQL_delete(SQL)
        return
    if ("SELECT" in sql) and ("ORDER BY" not in sql):
        SQL_sekect(SQL)
        return
    if "UPDATE" in sql:
        SQL_updata(SQL)
        return
    if ("SELECT" in sql) and ("ORDER BY" in sql):
        SQL_sort(SQL)
        return
    else:
        print("Wrong operate!!")
        return


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """"""


"""输入SQL语句"""


def Input_SQL() -> str:
    SQL_lines = []
    while True:
        SQL_line = input()
        if SQL_line == "":
            break
        SQL_lines.append(SQL_line)
    SQL_final = "  ".join(SQL_lines)
    return SQL_final


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """"""

add_table(
    "students",
    [
        Filed("id", FiledType.INT),
        Filed("name", FiledType.TEXT),
        Filed("age", FiledType.INT),
        Filed("gender", FiledType.TEXT),
    ],
)

add_row("students", {"id": 1, "name": "Alice", "age": 10, "gender": "female"})
add_row(
    "students",
    {"id": 3, "name": "Charlie", "age": 28, "gender": "male"},
)

add_row("students", {"id": 4, "name": "David", "age": 23, "gender": "male"})
