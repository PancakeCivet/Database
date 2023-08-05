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
Input_SQL()
down()
