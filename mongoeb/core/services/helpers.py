from mongoeb.core.services.query_builder import build_query, build_projection


def find_documents(
        db,
        collection: str,
        filters: list[str],
        include=None,
        exclude=None,
        no_id=False,
        one=False,
        limit=10
):
    query = build_query(filters)
    projection = build_projection(include, exclude)

    if no_id:
        projection = projection or {}
        projection["_id"] = 0

    if one:
        doc = db[collection].find_one(query, projection)
        return [doc] if doc else []
    else:
        return list(db[collection].find(query, projection).limit(limit))


def count_docs(db, collection: str) -> int:
    return db[collection].count_documents({})


def show_docs(db, collection: str, limit: int = 3) -> list:
    return list(db[collection].find().limit(limit))
