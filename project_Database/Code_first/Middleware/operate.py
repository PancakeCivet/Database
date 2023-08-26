import re
from typing import Any

from Database.Date_base import Database_table, Filed, FiledType


class Operator:
    @classmethod
    def Judge(cls, item: str) -> FiledType:
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

    @classmethod
    def judge(cls, item: str) -> FiledType:
        if item == "INT":
            return FiledType.INT
        elif item == "BOOLEAN":
            return FiledType.BOOLEAN
        elif item == "FLOAT":
            return FiledType.FLOAT
        elif item == "DATE":
            return FiledType.DATE
        else:
            return FiledType.TEXT

    @classmethod
    def SQL_add_table(cls, SQL: str, dat: Database_table) -> None:
        pattern = r"^CREATE TABLE (\w+) \((.+)\);?$"
        match = re.match(pattern, SQL, re.IGNORECASE)
        if match:
            table_name = match.group(1)
            column_info = match.group(2)
            column_pattern = r"(\w+) (\w+)(?:\((\d+)\))?(\s+\w+)?(,\s+|$)"
            columns = re.findall(column_pattern, column_info)
            Fileds: list[Filed] = []
            for column in columns:
                Fileds.append(Filed(column[0], cls.judge(column[1])))
            dat.add_table(table_name, Fileds)

    @classmethod
    def SQL_add(cls, SQL: str, dat: Database_table) -> None:
        pattern = r"INSERT INTO\s+(\w+)\s+VALUES\s+\((.*)\)"
        match = re.search(pattern, SQL, re.IGNORECASE)
        if match:
            table_name = match.group(1)
            values = [value.strip() for value in match.group(2).split(",")]
            dat.add_row(table_name, values)

    @classmethod
    def SQL_delete(cls, SQL: str, dat: Database_table) -> None:
        pattern = r"DELETE\s+FROM\s+(\w+)\s+WHERE\s+(.*)"
        match = re.search(pattern, SQL, re.IGNORECASE)
        if match:
            table_name = match.group(1)
            conditions = [value.strip() for value in match.group(2).split("=")]
            conditions[1] = conditions[1].strip("';")
            dat.delete(
                table_name, conditions[0], cls.Judge(conditions[1]), conditions[1]
            )

    @classmethod
    def SQL_sekect_all(cls, SQL: str, dat: Database_table) -> dict:
        pattern = r"SELECT\s+\*\s+FROM\s+(\w+)"
        match = re.match(pattern, SQL, re.IGNORECASE)
        if match:
            table_name = match.group(1)
            data = dat.Fin_all(table_name)
            return data

    @classmethod
    def SQL_sekect_part(cls, SQL: str, dat: Database_table) -> dict:
        pattern = r"SELECT\s+(.+)\s+FROM\s+(\w+)"
        match = re.match(pattern, SQL, re.IGNORECASE)
        if match:
            table_name = match.group(2)
            conditions = [value.strip() for value in match.group(1).split(",")]
            data = dat.Fin_part(table_name, conditions)
            return data

    @classmethod
    def SQL_sekect_or_part(cls, SQL: str, dat: Database_table) -> None:
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
            data = dat.Fin_condition_or(table_name, columns, condition_dict)
            return data

    @classmethod
    def SQL_sekect_and_part(cls, SQL: str, dat: Database_table):
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
            data = dat.Fin_condition_and(table_name, columns, condition_dict)
            return data

    @classmethod
    def SQL_sekect_condition(cls, SQL: str, dat: Database_table) -> None:
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
            data = dat.Fin_condition(table_name, columns, condition_dict)
            return data

    @classmethod
    def SQL_sekect(cls, SQL: str, dat: Database_table) -> dict:
        if "*" in SQL:
            data = cls.SQL_sekect_all(SQL, dat)
            return data
        elif "where" in SQL:
            if "or" in SQL:
                data = cls.SQL_sekect_or_part(SQL, dat)
                return data
            elif "and" in SQL:
                data = cls.SQL_sekect_and_part(SQL, dat)
                return data
            else:
                data = cls.SQL_sekect_condition(SQL, dat)
                return data
        else:
            data = cls.SQL_sekect_part(SQL, dat)
            return data

    @classmethod
    def SQL_updata(cls, SQL: str, dat: Database_table) -> None:
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
            print(cls.Judge(conditions[1]))
            dat.update(
                table_name,
                conditions[0],
                cls.Judge(conditions[1]),
                conditions[1],
                Updata,
            )

    @classmethod
    def SQL_sort(cls, SQL: str, dat: Database_table) -> None:
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
        dat.sql_sort(table_name[0], columns[0], order_by[0][0], order_by[0][1])

    @classmethod
    def analysis(cls, SQL: str, dat: Database_table) -> dict:
        sql = SQL.upper()
        if "INSERT INTO" in sql:
            cls.SQL_add(SQL, dat)
        elif "DELETE" in sql:
            cls.SQL_delete(SQL, dat)
        elif ("SELECT" in sql) and ("ORDER BY" not in sql):
            database_temp = cls.SQL_sekect(SQL, dat)
            return database_temp
        elif "UPDATE" in sql:
            cls.SQL_updata(SQL, dat)
        elif ("SELECT" in sql) and ("ORDER BY" in sql):
            cls.SQL_sort(SQL, dat)
        elif "CREATE TABLE" in sql:
            cls.SQL_add_table(SQL, dat)
        database_temp = {}
        for table_name, table_struct in dat.Table_dict.items():
            database_temp[table_name] = table_struct.json()
        return database_temp


if __name__ == "__main__":
    a = Database_table()
    a.extraction()
    Operator.analysis("delete from students where id = 1", a)
