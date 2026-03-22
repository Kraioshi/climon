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
    result = {}

    if not filters:
        return result

    for f in filters:
        if "=" not in f:
            raise ValueError(f"Invalid filter format: {f}. Use key=value")

        key, raw_value = f.split("=", 1)
        value = parse_value(raw_value)

        result[key] = value

    return result


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

# def build_query(filters: list[str]) -> dict[str, str]:
#     """
#     Construct a MongoDB query dict using CLI key-value pairs
#
#     Takes list of CLI arguments representing altering keys and values and transforms into dict.
#
#     Example:
#         input:
#             filters = ["benefit", "Free Will", "description", "Very descriptive"]
#
#         Output:
#             {
#                 "benefit": "Free Will",
#                 "description": "Very descriptive"
#             }
#
#     :param filters: list of CLI
#     :return: dict representing MongoDB query
#     """
#     query = {}
#
#     for i in range(0, len(filters), 2):
#         key = filters[i]
#         value = parse_value(filters[i + 1])
#         query[key] = value
#
#     return query
