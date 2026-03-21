import rich
from dotenv import load_dotenv

from mongoeb.core.printer import print_table, print_json, print_compact

from mongoeb.core.config import load_config

import typer
from pymongo import MongoClient

from mongoeb.core.uri import build_uri
from mongoeb.core.validators import InputValidator

from mongoeb.core.db import get_db

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
        results = db.list_collection_names()
        rich.print(sorted(results))


def main():
    load_dotenv()
    app()


if __name__ == "__main__":
    main()
