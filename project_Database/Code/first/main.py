import json
import pprint
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


"""
数据库本身
"""

Table_dict: dict[str, Table_struct] = {}
"""建立字典，运用字典的key对应表的name找到表所对应的Table_struct"""


"""
operate部分
"""

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
    table_data = {}
    table_data = Table_dict[table_name].json()


"""只要部分的字段"""


def Fin_part(table_name: str, column_name: list[str]):
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
    pprint.pprint(table_temp)


"""查满足条件的"""

def Fin_condition(table_name:str,):
    

"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """"""


"""改"""


def update(
    table_name: str, column_name: str, content: FiledType, Update: list[dict[str:Any]]
) -> None:
    """传入的参数：表名，字段名，字段名对应的类型，修改的数据"""
    if table_name in Table_dict:
        element = Table_dict[table_name]
        for row in element.filed_row:
            if column_name in row:
                for last in Table_dict[table_name].filed_column:
                    if last.name == column_name and content == last.type:
                        for item in Update:
                            for key, value in item.items():
                                if key in row:
                                    row[key] = value
                        return
    print("Wrong operate!!")


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """"""


"""删"""


def delete(
    table_name: str, column_name: str, content: FiledType, condition: Any
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
                        return
    print("Wrong operate!!")


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """"""


"""将数据库保存为JSON文件"""


def down() -> None:
    path = Path("E:/Code/project_Database/Date")
    file = path / "database.json"
    database_temp = {}
    for table_name, table_struct in Table_dict.items():
        database_temp[table_name] = table_struct.json()
    with open(file, "w", encoding="utf-8") as f:
        json.dump(database_temp, f, ensure_ascii=False)
    Table_dict.clear()


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """"""

"""提取JSON文件"""


def extraction() -> None:
    path = Path("E:/Code/project_Database/Date")
    file = path / "database.json"
    database_temp = {}
    with open(file, "r", encoding="utf-8") as f:
        database_temp = json.load(f)
    for table_name, table_data in database_temp.items():
        table_struct = Table_struct()
        table_struct.load(table_data)
        Table_dict[table_name] = table_struct


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """"""
