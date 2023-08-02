add_table(
    "students",
    [
        Filed("id", FiledType.INT),
        Filed("name", FiledType.TEXT),
        Filed("age", FiledType.INT),
        Filed("gender", FiledType.TEXT),
    ],
)

add_row("students", {"id": 1, "name": "Alice", "age": 20, "gender": "female"})
add_row(
    "students",
    {"id": 3, "name": "Charlie", "age": 21, "gender": "male"},
)

add_row("students", {"id": 4, "name": "David", "age": 23, "gender": "male"})

update(
    "students",
    "name",
    FiledType.TEXT,
    [{"id": 1, "name": "Bob"}, {"id": 2, "name": "Charlie"}],
)

delete("students", "age", FiledType.INT, 20)

down()
extraction()

print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")

Fin_part(
    "students",
    ["name", "Id", "age"],
)
