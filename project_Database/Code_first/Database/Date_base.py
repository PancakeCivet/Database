import json
import os
from enum import Enum
from pathlib import Path
from typing import Any


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

    def loads(self, data: dict) -> None:
        self.name = data["name"]
        for element in data["filed_column"]:
            self.filed_column.append(Filed(element["name"], FiledType(element["type"])))
        self.filed_row = data["filed_row"]

    """将JSON格式转为类"""


class Database_table:
    Table_dict: dict[str, Table_struct] = {}

    def __init__(self) -> None:
        self.Table_dict.clear()

    def add_table(self, table_name: str, content: list[Filed]) -> None:
        self.Table_dict[table_name] = Table_struct()
        self.Table_dict[table_name].name = table_name
        self.Table_dict[table_name].filed_column = content
        self.Table_dict[table_name].filed_column.insert(0, Filed("Id", FiledType.INT))

    def add_row(self, table_name: str, values: list) -> None:
        if table_name in self.Table_dict:
            content = {}
            temp_tot = 0
            for element in self.Table_dict[table_name].filed_column:
                if element.name == "Id":
                    Id_ = len(self.Table_dict[table_name].filed_row)
                    content["Id"] = Id_
                else:
                    content[element.name] = values[temp_tot]
                    temp_tot += 1
            Id = len(self.Table_dict[table_name].filed_row)
            content["Id"] = Id
            self.Table_dict[table_name].filed_row.append(content)

    def Fin_all(self, table_name: str) -> dict:
        if table_name in self.Table_dict:
            table_data = {}
            table_data = self.Table_dict[table_name].json()
            return table_data

    def Fin_part(self, table_name: str, column_name: list[str]) -> dict:
        if table_name in self.Table_dict:
            table_data = Table_struct()
            table_temp = {}
            table_data.name = table_name
            for element in column_name:
                for i in range(len(self.Table_dict[table_name].filed_row)):
                    table_data.filed_row.append(
                        {element: self.Table_dict[table_name].filed_row[i][element]}
                    )
            for element in column_name:
                for item in self.Table_dict[table_name].filed_column:
                    if element == item.name:
                        table_data.filed_column.append(item)
            table_temp = table_data.json()
            return table_temp

    def Fin_condition(
        self, table_name: str, column_name: list[str], condition: dict[str, Any]
    ) -> dict:
        if table_name in self.Table_dict:
            table_data = Table_struct()
            table_temp = {}
            table_data.name = table_name
            keys = condition.keys()
            key_list = list(keys)
            key_condition = key_list[0]
            for row in self.Table_dict[table_name].filed_row:
                if str(row[key_condition]) == str(condition[key_condition]):
                    for element in column_name:
                        table_data.filed_row.append({element: row[element]})
                    for element in column_name:
                        for item in self.Table_dict[table_name].filed_column:
                            if element == item.name:
                                table_data.filed_column.append(item)
            table_temp = table_data.json()
            return table_temp

    def Fin_condition_and(
        self,
        table_name: str,
        column_name: list[str],
        conditions: list[dict[str, Any]],
    ) -> dict:
        """condition_names中key与value相同"""
        if table_name in self.Table_dict:
            table_data = Table_struct()
            table_temp = {}
            table_data.name = table_name
            flag_column = True
            for row in self.Table_dict[table_name].filed_row:
                """对每个数据枚举"""
                flag = 0
                for column in self.Table_dict[table_name].filed_column:
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
                            for item in self.Table_dict[table_name].filed_column:
                                if element == item.name:
                                    table_data.filed_column.append(item)
            table_temp = table_data.json()
            return table_temp

    def Fin_condition_or(
        self,
        table_name: str,
        column_name: list[str],
        conditions: list[dict[str, Any]],
    ) -> dict:
        """condition_names中key与value相同"""
        if table_name in self.Table_dict:
            table_data = Table_struct()
            table_temp = {}
            table_data.name = table_name
            flag_column = True
            for row in self.Table_dict[table_name].filed_row:
                """对每个数据枚举"""
                flag = 0
                for column in self.Table_dict[table_name].filed_column:
                    for condition in conditions:
                        if column.name in condition:
                            if str(row[column.name]) == str(condition[column.name]):
                                flag += 1
                if flag > 0:
                    for element in column_name:
                        table_data.filed_row.append({element: row[element]})
                    if flag_column:
                        flag_column = False
                        for element in column_name:
                            for item in self.Table_dict[table_name].filed_column:
                                if element == item.name:
                                    table_data.filed_column.append(item)
            table_temp = table_data.json()
            return table_temp

    def sql_sort(
        self,
        table_name: str,
        column_name: list[str],
        column_condition: str,
        direction: str,
    ):
        if table_name in self.Table_dict:
            table_data = Table_struct()
            table_temp = {}
            row_data = []
            table_data.name = table_name
            for row in self.Table_dict[table_name].filed_row:
                row_data.append(row[column_condition])
            combined = list(zip(row_data, self.Table_dict[table_name].filed_row))
            if direction == "DESC":
                combined.sort(key=lambda x: x[0], reverse=True)
            else:
                combined.sort(key=lambda x: x[0], reverse=False)
            row_data, self.Table_dict[table_name].filed_row = zip(*combined)
            for row in self.Table_dict[table_name].filed_row:
                for element in column_name:
                    table_data.filed_row.append({element: row[element]})
            for element in column_name:
                for item in self.Table_dict[table_name].filed_column:
                    if element == item.name:
                        table_data.filed_column.append(item)
            table_temp = table_data.json()

    def update(
        self,
        table_name: str,
        column_name: str,
        content: FiledType,
        row_column_name: str,
        Update: list[dict[str, Any]],
    ) -> None:
        """传入的参数：表名，字段名，字段名对应的类型，条件，修改的数据"""
        if table_name in self.Table_dict:
            element = self.Table_dict[table_name]
            i = 0
            for row in element.filed_row:
                if column_name in row:
                    for last in self.Table_dict[table_name].filed_column:
                        if (
                            (last.name == column_name)
                            and (content == last.type)
                            and (row_column_name == str(row[column_name]))
                        ):
                            for item in Update:
                                for key, value in item.items():
                                    if key in row:
                                        self.Table_dict[table_name].filed_row[i][
                                            key
                                        ] = value
                i += 1

    def delete(
        self, table_name: str, column_name: str, content: FiledType, condition: str
    ) -> None:
        """传入的参数：表名，字段名，字段名对应的类型，字段名下数据"""
        if table_name in self.Table_dict:
            element = self.Table_dict[table_name]
            for row in element.filed_row:
                if str(row[column_name]) == condition:
                    for last in self.Table_dict[table_name].filed_column:
                        if last.name == column_name and content == last.type:
                            element.filed_row.remove(row)
                            for i in range(len(element.filed_row)):
                                element.filed_row[i]["Id"] = i

    def down(self) -> None:
        current_dir = os.getcwd()
        folder_path = os.path.join(current_dir, "Date")
        os.makedirs(folder_path, exist_ok=True)
        file = os.path.join(folder_path, "database.JSON")
        database_temp = {}
        for table_name, table_struct in self.Table_dict.items():
            database_temp[table_name] = table_struct.json()
        with open(file, "w", encoding="utf-8") as f:
            json.dump(database_temp, f, ensure_ascii=False)
        self.Table_dict.clear()

    def extraction(self) -> None:
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
            self.Table_dict[table_name] = table_struct


if __name__ == "__main__":
    a = Database_table()
    a.add_table(
        "students",
        [
            Filed("id", FiledType.INT),
            Filed("name", FiledType.TEXT),
            Filed("age", FiledType.INT),
            Filed("gender", FiledType.TEXT),
        ],
    )

    a.add_row("students", [1, "Alice", 10, "female"])
    a.add_row(
        "students",
        [3, "Charlie", 28, "male"],
    )
    a.down()
