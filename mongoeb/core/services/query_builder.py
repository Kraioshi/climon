from datetime import datetime


def parse_value(value: str) -> int | float | bool | datetime | str:
    """
    Convert string CLI input into appropriate Python type.

    Attempts to get the most suitable type for a given string value.

    Order:
    1. Integer ("69" -> 69)
    2. Float ("3.14" -> 3.14)
    3. Bool ("true" -> True, "false" -> False)
    4. Datetime (ISO string -> datetime obj)
    5. Fallback (remains string)

    Important:
    Datetime parsing uses `datetime.fromisoformat`, so input most follow ISO format

    :param value: Raw string value from CLI.
    :return: Parse value in appropriate Python type.
    """
    if value.isdigit():
        return int(value)
    try:
        return float(value)
    except ValueError:
        pass
    if value.lower() in ["true", "false"]:
        return value.lower() == "true"

    try:
        return datetime.fromisoformat(value)
    except ValueError:
        pass

    return value


def build_query(filters: list[str]) -> dict[str, str]:
    """
    Construct a MongoDB query dict using CLI key-value pairs

    Takes list of CLI arguments representing altering keys and values and transforms into dict.

    Example:
        input:
            filters = ["benefit", "Free Will", "description", "Very descriptive"]

        Output:
            {
                "benefit": "Free Will",
                "description": "Very descriptive"
            }

    :param filters: list of CLI
    :return: dict representing MongoDB query
    """
    query = {}

    for i in range(0, len(filters), 2):
        key = filters[i]
        value = parse_value(filters[i + 1])
        query[key] = value

    return query


def build_projection(fields: list[str] | None, ignore: list[str] | None) -> dict[str, int] | None:
    """
    Build a MongoDB projection dictionary from CLI inputs.

    Supports:
       1. Inclusion (--fields):
           ["name", "age"] -> {"name": 1, "age": 1}

       2. Exclusion mode (--ignore):
           ["password"] -> {"password": 0}

    Rules:
       - Cannot use both `fields` and `ignore` at the same time
       - MongoDB doesn't allow mixing inclusion (1) and exclusion (0),
         except for the "_id" field.

    Behavior:
       - If `fields` provided -> inclusion projection
       - If `ignore` provided -> exclusion projection
       - If neither -> returns None (no projection)

    :param fields: List of field names to include
    :param ignore: List of field names to exclude
    :return: MongoDB projection dict or None
    :raises ValueError: If both fields and ignore are provided
    """
    if fields and ignore:
        raise ValueError("Can't use --fields and --ignore together!")

    if fields:
        projection = {field: 1 for field in fields}
        return projection

    if ignore:
        projection = {ignored_field: 0 for ignored_field in ignore}
        return projection

    return None
