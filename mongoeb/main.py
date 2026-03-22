import shlex

import rich
from dotenv import load_dotenv

from mongoeb.core.printer import print_output

import typer

from mongoeb.core.services.query_builder import parse_filters, normalize_fields, normalize_filters
from mongoeb.core.validators import InputValidator

from mongoeb.core.db import get_db
from mongoeb.core.services.helpers import count_docs, show_docs, find_documents, split_sections

load_dotenv()

app = typer.Typer()
validator = InputValidator()


@app.command("health")
def health_check():
    """
    Basic sanity check to verify CLI is working.

    Usage:
        mongoeb health
    """
    rich.print("Mongoeb is Mongoebing!")


# recreate config on every call atm.
# Later create once and pass w/ context?

@app.command("show-collections")
def show_collections() -> None:
    """
    List all collections in the database (sorted alphabetically).

    Usage:
        mongoeb show-collections
    """
    with get_db() as db:
        results = list(db.list_collection_names())
        rich.print(sorted(results))


@app.command("show")
def show(collection: str, limit: int = 3, output_format: str | None = None) -> None:
    """
    Display documents from a collection.

    By default, returns up to 3 documents.

    Usage:
        mongoeb show employees
        mongoeb show employees --limit 5
        mongoeb show employees --output-format pretty 💅

    :param collection: Name of the MongoDB collection
    :param limit: Maximum number of documents to return
    :param output_format: Output format ("pretty", "table", "compact")
    """
    validator.validate_collection_name(collection)
    validator.validate_limit(limit)
    with get_db() as db:
        docs = show_docs(db=db, collection=collection, limit=limit)

    print_output(docs, collection, output_format)


@app.command("count")
def count(collection: str) -> None:
    """
    Count total number of documents in a collection.

    :param collection: Name of the MongoDB collection

    Usage:
        mongoeb count collection_name
    """
    validator.validate_collection_name(collection)
    with get_db() as db:
        document_count = count_docs(db=db, collection=collection)

    rich.print(f"{collection} count: ", document_count)


## Multiple parameter support
@app.command("find")
def find_one_or_many(
        collection: str,
        filters: list[str] = typer.Option(None, "--filter"),
        include: list[str] = typer.Option(None, "--include"),
        exclude: list[str] = typer.Option(None, "--exclude"),
        no_id: bool = typer.Option(False, "--no-id"),
        one: bool = typer.Option(False, "--one"),
        limit: int = typer.Option(10),
        output_format: str | None = None) -> None:
    """
    Find documents in a collection using key-value filters.

    Filters are provided as pairs:
        `field` `value`

    Supports multiple filters (AND logic).

    Projection:
    - Use --include to include only specific fields
    - Use --exclude to exclude specific fields
    - Use --no-id to exclude the '_id' field

    ⚠️ Field input formats.
    Multiple input formats are supported:
    1. Repeated flags:
        --include company --include salary
    2. Comma separated values:
        --include "company, salary"
    3. Space separated values:
        --include "company salary"
    4. Mixed format:
        --include "company, salary" --include work_email

    ⚠️ Important:
    - --include and --exclude can't be used together
    - MongoDB doesn't allow mixing inclusion and exclusion (except for id)

    Usage:
        # Basic
        mongoeb find employees name Nameless
        mongoeb find employees name Nameless age 30
        mongoeb find employees name Nameless --limit 5
        mongoeb find employees name Nameless --one

        # Projection examples
        mongoeb find employees name Nameless --include name age
        mongoeb find employees name Nameless --exclude job
        mongoeb find employees name Nameless --include name age --no-id

        # Output formatting
        mongoeb find employees name Nameless --output-format table
        mongoeb find employees name Nameless --output-format pretty

    :param collection: Name of the MongoDB collection
    :param filters: Key-value pairs (must be even number of arguments)
    :param include: Fields to include in result (inclusion projection)
    :param exclude: Fields to exclude from result (exclusion projection)
    :param no_id: Exclude "_id" field from results
    :param limit: Maximum number of documents to return (excluded if --one is used)
    :param one: Return only a single document (uses find_one)
    :param output_format: Output format ("pretty", "table", "compact")
    """

    validator.validate_collection_name(collection)
    validator.validate_filters(filters)
    validator.validate_limit(limit)

    with get_db() as db:
        include_fields = normalize_fields(include)
        exclude_fields = normalize_fields(exclude)
        filters_dict = parse_filters(filters)
        result = find_documents(db, collection, filters_dict, include_fields, exclude_fields, no_id, one, limit)
    print_output(docs=result, output_format=output_format, collection=collection)


@app.command("shell")
def shell():
    with get_db() as db:
        while True:
            try:
                cmd = input("mongoeb > ")

                if cmd in ["exit", "quit", "zaebal"]:
                    break

                # Temporary naive parsing
                parts = shlex.split(cmd)
                # print(parts)
                if not parts:
                    continue

                result = handle_commands(db, parts)

                command = parts[0]
                if command == "count":
                    collection = parts[1]
                    rich.print(f"{collection} count: {result}")
                elif command == "show-collections":
                    print_output(docs=result, collection="collections")

                elif command in ["show", "find"]:
                    collection = parts[1]
                    print_output(result, collection)
                else:
                    print_output(result, collection)

            except Exception as e:
                rich.print(f"[red]Error:[/red] {e}")


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



def main():
    load_dotenv()
    app()


if __name__ == "__main__":
    main()
