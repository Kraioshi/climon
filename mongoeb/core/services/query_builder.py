from datetime import datetime
from bson import ObjectId


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
    # int
    try:
        return int(value)
    except ValueError:
        pass

    # float
    try:
        return float(value)
    except ValueError:
        pass

    # bool
    if value.lower() in ["true", "false"]:
        return value.lower() == "true"

    # datetime
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        pass

    return value


def parse_filters(filters: list[str]) -> dict:
    """
    Convert ['a=b', 'c=d'] -> {'a': 'b', 'c': 'd'}.
    """
    conditions = []

    # result = {}

    for f in filters:
        if "=" not in f:
            raise ValueError(
                f"Invalid filter '{f}'. Expected format: field=value"
            )

        key, raw_value = f.split("=", 1)

        condition = build_field_filter(key, raw_value)
        conditions.append(condition)

    if not conditions:
        return {}

    if len(conditions) == 1:
        return conditions[0]

    return {"$and": conditions}


def normalize_fields(fields: list[str] | None) -> list[str] | None:
    """
    Normalize field input into a flat list of field names

    Supports multiple input formats
    1. Repeated flags:
        --include company --include salary
    2. Comma separated values:
        --include "company, salary"
    3. Space separated values:
        --include "company salary"
    4. Mixed format:
        --include "company, salary" --include work_email

    :param fields: Raw CLI input list
    :return: Normalized list of fields or None
    """
    if fields is None:
        return None

    result = []

    for field in fields:
        # COMMA SEPARATED SUPPORT
        parts = field.split(",")

        for part in parts:
            # SPACE SEPARATED SUPPORT
            supported = part.strip().split()
            result.extend(supported)

    return result

def normalize_filters(filters: list[str] | None) -> list[str]:
    """
    Normalize filter input into a flat list of 'field=value' strings.

    Supports:
    - CLI:
        --filter a=b --filter c=d
        --filter "a=b,c=d"

    - Shell:
        a=b c=d
        "a=b c=d"
        a=b,c=d
    """

    if not filters:
        return []

    result = []

    for f in filters:
        # split by comma first
        parts = f.split(",")

        for part in parts:
            cleaned = part.strip()

            if not cleaned:
                continue

            result.append(cleaned)

    return result


def build_projection(include: list[str] | None, exclude: list[str] | None) -> dict[str, int] | None:
    """
    Build a MongoDB projection dictionary from CLI inputs.

    Supports:
       1. Inclusion (--include):
           ["name", "age"] -> {"name": 1, "age": 1}

       2. Exclusion mode (--exclude):
           ["password"] -> {"password": 0}

    Rules:
       - Cannot use both `include` and `exclude` at the same time
       - MongoDB doesn't allow mixing inclusion (1) and exclusion (0),
         except for the "_id" field.

    Behavior:
       - If `include` provided -> inclusion projection
       - If `exclude` provided -> exclusion projection
       - If neither -> returns None (no projection)

    :param include: List of field names to include
    :param exclude: List of field names to exclude
    :return: MongoDB projection dict or None
    :raises ValueError: If both include and exclude are provided
    """
    if include and exclude:
        raise ValueError("Can't use --include and --exclude together!")

    if include:
        projection = {included_field: 1 for included_field in include}
        return projection

    if exclude:
        projection = {excluded_field: 0 for excluded_field in exclude}
        return projection

    return None


def build_field_filter(key: str, value: str) -> dict:
    """
    Build filter for a single field.

    ObjectId x string dual support.
    Plain value fallback
    """
    if ObjectId.is_valid(value):
        return {
            "$or": [
                {key: ObjectId(value)},
                {key: value}
            ]
        }
    return {key: value}