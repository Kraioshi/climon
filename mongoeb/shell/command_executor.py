from mongoeb.core.services.query_builder import parse_filters, normalize_fields, normalize_filters
from mongoeb.core.services.helpers import count_docs, show_docs, find_documents, split_sections


def handle_commands(db, parts: list):
    cmd = parts[0]

    if cmd == "count":
        if len(parts) < 2:
            raise ValueError("Missing collection name")
        collection = parts[1]
        return count_docs(db, collection)

    elif cmd == "show":
        collection = parts[1]
        return show_docs(db, collection)

    elif cmd == "show-collections":
        return list(db.list_collection_names())

    elif cmd == "find":
        # if len(parts) < 3:
        #     raise ValueError("Usage: find <collection> <filters>")

        sections = split_sections(parts)

        base = sections[0]

        if len(base) < 2:
            raise ValueError("Missing collection name")

        collection = base[1]
        raw_filters = base[2:]

        normalized_filters = normalize_filters(raw_filters)
        filters_dict = parse_filters(normalized_filters)

        include = None
        exclude = None
        limit = 10
        one = False

        # --- MODIFIERS ---
        for section in sections[1:]:
            cmd = section[0]

            if cmd == "include":
                include = normalize_fields(section[1:])

            elif cmd == "exclude":
                exclude = normalize_fields(section[1:])

            elif cmd == "limit":
                limit = int(section[1])

            elif cmd == "one":
                one = True

            else:
                raise ValueError(f"Unknown modifier: {cmd}")

        return find_documents(
            db,
            collection,
            filters=filters_dict,
            include=include,
            exclude=exclude,
            no_id=False,
            one=one,
            limit=limit,
        )

    else:
        raise ValueError(f"Unknown command: {cmd}")
