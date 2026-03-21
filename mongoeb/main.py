import rich
from dotenv import load_dotenv

from mongoeb.core.printer import print_table, print_json, print_compact, print_output

from mongoeb.core.config import load_config

import typer
from pymongo import MongoClient

from mongoeb.core.uri import build_uri
from mongoeb.core.validators import InputValidator

from mongoeb.core.db import get_db
from mongoeb.core.services.query_builder import build_query, parse_value

load_dotenv()

app = typer.Typer()
validator = InputValidator()


@app.command()
def health_check():
    print(f"Why am I here?")


# recreate config on every call atm.
# Later create once and pass w/ context?

@app.command()
def show(collection: str, limit: int = 1, output_format: str | None = None) -> None:
    config = load_config()
    uri = build_uri(config)
    validator.validate_collection_name(collection)
    validator.validate_limit(limit)
    client = MongoClient(uri)
    try:
        db = client[config.database]
        results = db[collection].find().limit(limit)
        docs = list(results)

        match output_format:
            case "pretty":
                print_json(docs)
            case "table":
                print_table(docs, collection)
            case "compact":
                print_compact(docs)
            case _:
                print_json(docs)

    finally:
        client.close()

@app.command()
def count(collection: str):
    config = load_config()
    uri = build_uri(config)
    validator.validate_collection_name(collection)
    client = MongoClient(uri)
    try:
        db = client[config.database]
        results = db[collection].count_documents({})
        rich.print(f"{collection} count: " ,results)
    finally:
        client.close()


@app.command()
def show_collections():
    with get_db() as db:
        results = list(db.list_collection_names())
        rich.print(sorted(results))

## Multiple parameter support
@app.command("find")
def find_one_or_many(
        collection: str,
        filters: list[str],
        limit: int = typer.Option(10),
        one: bool = typer.Option(False, "--one"),
        output_format: str | None = None) -> None:

    validator.validate_collection_name(collection)
    validator.validate_filters(filters)
    validator.validate_limit(limit)

    query = build_query(filters)
    with get_db() as db:
        if one:
            doc = db[collection].find_one(query)
            result = [doc] if doc else []
        else:
            result = list(db[collection].find(query).limit(limit))

    print_output(docs=result, output_format=output_format, collection=collection)


def main():
    load_dotenv()
    app()


if __name__ == "__main__":
    main()
