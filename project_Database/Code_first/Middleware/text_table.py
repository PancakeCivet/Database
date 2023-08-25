import re

create_table = "CREATE TABLE customers (id INT, name VARCHAR(255), email VARCHAR(255));"

pattern = r"^CREATE TABLE (\w+) \((.+)\);?$"

match = re.match(pattern, create_table)

table_name = match.group(1)
column_info = match.group(2)

column_pattern = r"(\w+) (\w+)(?:\((\d+)\))?(\s+\w+)?(,\s+|$)"


columns = re.findall(column_pattern, column_info)


print("Table Name:", table_name)
print("Columns:")
for column in columns:
    print(column[0], column[1])
