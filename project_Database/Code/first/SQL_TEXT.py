import re


def parse_select(sql):
    pattern = r"SELECT\s+(.+)\s+FROM\s+(\w+)\s+WHERE\s+(.+);$"
    match = re.search(pattern, sql)

    if match:
        select_columns = match.group(1)
        table_name = match.group(2)
        condition = match.group(3)
        print("Select columns:", select_columns)
        print("Table name:", table_name)
        print("Condition:", condition)
    else:
        print("Invalid SQL statement.")


# 示例SQL语句
sql_statement = "SELECT id, name FROM Websites WHERE country = 'CN';"

# 解析SELECT部分
parse_select(sql_statement)
