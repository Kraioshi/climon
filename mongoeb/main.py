import rich
from dotenv import load_dotenv

from mongoeb.core.printer import print_output

import typer

from mongoeb.core.validators import InputValidator

from mongoeb.core.db import get_db
from mongoeb.core.services.query_builder import build_query, build_projection

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
        results = db[collection].find().limit(limit)
        docs = list(results)

    print_output(docs, collection, output_format)


@app.command("count")
def count(collection: str) -> None:
    """
    Count total number of documents in a collection.

    :param collection: Name of the MongoDB collection

    Usage:
        mongoeb count collection
    """
    validator.validate_collection_name(collection)
    with get_db() as db:
        document_count = db[collection].count_documents({})

    rich.print(f"{collection} count: ", document_count)


## Multiple parameter support
@app.command("find")
def find_one_or_many(
    collection: str,
    filters: list[str],
    fields: list[str] = typer.Option(None, "--fields"),
    ignore: list[str] = typer.Option(None, "--ignore"),
    no_id: bool = typer.Option(False, "--no-id"),
    one: bool = typer.Option(False, "--one"),
    limit: int = typer.Option(10),
    output_format: str | None = None) -> None:
    """
    Find documents in a collection using key-value filters.

    Filters are provided as pairs:
        <field> <value>

    Supports multiple filters (AND logic).

    Projection:
    - Use --fields to include only specific fields
    - Use --ignore to exclude specific fields
    - Use --no-id to exclude the '_id' field

    Important:
    - --fields and --ignore can't be used together
    - MongoDB doesn't allow mixing inclusion and exclusion (except for id)

    Usage:
        # Basic
        mongoeb find employees name Nameless
        mongoeb find employees name Nameless age 30
        mongoeb find employees name Nameless --limit 5
        mongoeb find employees name Nameless --one

        # Projection examples
        mongoeb find employees name Nameless --fields name age
        mongoeb find employees name Nameless --ignore job
        mongoeb find employees name Nameless --fields name age --no-id

        # Output formatting
        mongoeb find employees name Nameless --output-format table
        mongoeb find employees name Nameless --output-format pretty

    :param collection: Name of the MongoDB collection
    :param filters: Key-value pairs (must be even number of arguments)
    :param fields: Fields to include in result (inclusion projection)
    :param ignore: Fields to exclude from result (exclusion projection)
    :param no_id: Exclude "_id" field from results
    :param limit: Maximum number of documents to return (ignored if --one is used)
    :param one: Return only a single document (uses find_one)
    :param output_format: Output format ("pretty", "table", "compact")
    """

    validator.validate_collection_name(collection)
    validator.validate_filters(filters)
    validator.validate_limit(limit)

    query = build_query(filters)
    projection = build_projection(fields, ignore)
    if no_id:
        # prevent crash if projection is None
        projection = projection or {}
        projection["_id"] = 0

    with get_db() as db:
        if one:
            doc = db[collection].find_one(query, projection)
            result = [doc] if doc else []
        else:
            result = list(db[collection].find(query, projection).limit(limit))

    print_output(docs=result, output_format=output_format, collection=collection)


def main():
    load_dotenv()
    app()


if __name__ == "__main__":
    main()
