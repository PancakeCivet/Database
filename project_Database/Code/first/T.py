class FiledType(str, Enum):
    """字段数据类型"""

    INT = "INT"
    FLOAT = "FLOAT"
    TEXT = "TEXT"
    BOOLEAN = "BOOLEAN"
    DATE = "DATE"


def Judge(item: str) -> FiledType:
    if ("false" in item) or ("true" in item):
        return FiledType.BOOLEAN
    elif "-" in item:
        return FiledType.DATE
    elif "." in item:
        return FiledType.FLOAT
    elif item.isdigit():
        return FiledType.INT
    else:
        return FiledType.TEXT
