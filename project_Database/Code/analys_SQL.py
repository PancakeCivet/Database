import json
import os
import pickle
import pprint
import re
import socket
from enum import Enum
from pathlib import Path
from typing import Any

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


def SQL_sekect_all(SQL: str):
    pattern = r""


def SQL_sekect_or_all(SQL: str):
    pass


def SQL_sekect_and_all(SQL: str):
    pass


def SQL_sekect_part(SQL: str):
    pass


def SQL_sekect_or_part(SQL: str):
    pass


def SQL_sekect_and_part(SQL: str):
    pass


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """"""


"""分治"""


def SQL_sekect_or(SQL: str) -> None:
    if "*" in SQL:
        SQL_sekect_or_all(SQL)
    else:
        SQL_sekect_or_part(SQL)


def SQL_sekect_and(SQL: str) -> None:
    if "*" in SQL:
        SQL_sekect_and_all(SQL)
    else:
        SQL_sekect_and_part(SQL)


def SQL_sekect(SQL: str) -> None:
    if "or" in SQL:
        SQL_sekect_or(SQL)
    elif "and" in SQL:
        SQL_sekect_and(SQL)
    elif "*" in SQL:
        SQL_sekect_all(SQL)
    else:
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
        update(table_name, conditions[0], Judge(conditions[1]), conditions[1], Updata)


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


def Input_SQL() -> None:
    SQL_lines = []
    while True:
        SQL_line = input()
        if SQL_line == "":
            break
        SQL_lines.append(SQL_line)
    SQL_final = "  ".join(SQL_lines)
    analysis(SQL_final)


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

down()

extraction()
