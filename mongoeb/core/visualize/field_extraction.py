from typing import Any

from mongoeb.core.visualize.type_detection import  detect_type

def extract_fields(doc: dict, field_map: dict[str, Any], prefix: str = "") -> None:
    for key, value in doc.items():

        field_name = f"{prefix}.{key}" if prefix else key

        # Add field if doesn't exist
        if field_name not in field_map:
            field_map[field_name] = {
                "count": 0,
                "types": {}
            }
        # update count
        field_map[field_name]["count"] += 1

        # Try to detect type :)
        t = detect_type(value)
        field_map[field_name]["types"][t] = field_map[field_name]["types"].get(t, 0) + 1

        # Recursion stuff
        if isinstance(value, dict):
            extract_fields(value, field_map, field_name)

        elif isinstance(value, list):
            # Check first element
            if value:
                first = value[0]
                if isinstance(first, dict):
                    extract_fields(first, field_map, f"{field_name}[]")
