from datetime import datetime

def parse_value(value: str):
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

def build_query(filters: list[str]) -> dict:
    query = {}

    for i in range(0, len(filters), 2):
        key = filters[i]
        value = parse_value(filters[i + 1])
        query[key] = value

    return query