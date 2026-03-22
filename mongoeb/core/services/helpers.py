from mongoeb.core.services.query_builder import build_projection, normalize_fields, parse_filters


def find_documents(
        db,
        collection: str,
        filters: dict[str, object],
        include: list[str] | None = None,
        exclude: list[str] | None = None,
        no_id=False,
        one=False,
        limit=10
):
    projection = build_projection(include, exclude)

    if no_id:
        projection = projection or {}
        projection["_id"] = 0

    if one:
        doc = db[collection].find_one(filters, projection)
        return [doc] if doc else []
    else:
        return list(db[collection].find(filters, projection).limit(limit))


def count_docs(db, collection: str) -> int:
    return db[collection].count_documents({})


def show_docs(db, collection: str, limit: int = 3) -> list:
    return list(db[collection].find().limit(limit))


def split_sections(parts: list[str]):
    sections = []
    current = []

    for part in parts:
        if part == "|":
            sections.append(current)
            current = []
        else:
            current.append(part)

    if current:
        sections.append(current)

    return sections
