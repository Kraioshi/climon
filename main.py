from dotenv import load_dotenv

from core.printer import print_table, print_json, print_compact

from core.config import load_config

import typer
from pymongo import MongoClient

from core.uri import build_uri
from core.validators import InputValidator

load_dotenv()

app = typer.Typer()
validator = InputValidator()


@app.command()
def health_check():
    print(f"Why am I here?")


# recreate config on every call atm.
# Later create once and pass w/ context?

@app.command()
def show(collection: str, limit: int, output_format: str | None = None):
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


if __name__ == "__main__":
    app()
