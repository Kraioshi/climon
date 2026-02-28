from dotenv import load_dotenv
import pprint

from core.config import load_config

import typer
from pymongo import MongoClient

from core.uri import build_uri
from core.validators import InputValidator
app = typer.Typer()
validator = InputValidator()

@app.command()
def health_check():
    print(f"Why am I here?")

# recreate config on every call atm.
# Later create once and pass w/ context?

@app.command()
def show(collection: str, limit: int):
    config = load_config()
    uri = build_uri(config)
    validator.validate_collection_name(collection)
    validator.validate_limit(limit)
    client = MongoClient(uri)
    try:
        db = client[config.database]
        results = db[collection].find().limit(limit)
        for r in results:
            pprint.pp(r)
    finally:
        client.close()

if __name__ == "__main__":
    load_dotenv()
    app()