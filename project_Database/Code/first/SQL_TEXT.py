import re


def parse_select(sql):
    pattern = r"SELECT\s+(.+)\s+FROM\s+(\w+)\s+WHERE\s+(.+)$"
    match = re.search(pattern, sql, re.IGNORECASE)

    if match:
        select_columns = match.group(1)
        table_name = match.group(2)
        conditions = match.group(3)
        print("Select columns:", select_columns)
        print("Table name:", table_name)
        print("Conditions:", conditions)
    else:
        print("Invalid SQL statement.")


# 示例SQL语句
sql_statement = "select id,name  from students  where Id = 1 or id = 1"
# sql_statement = "SELECT id,name FROM Websites WHERE country='CN' or Id = 1"

# 解析SELECT部分
parse_select(sql_statement)
