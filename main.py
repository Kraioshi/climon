import os
from dotenv import load_dotenv
import pprint

load_dotenv()

db_name = os.getenv("M_DATABASE")

import typer
from pymongo import MongoClient

from core.uri import load_uri
app = typer.Typer()

@app.command()
def health_check():
    print(f"Why am I here?")

@app.command()
def show(collection: str, limit: int):
    uri = load_uri()
    client = MongoClient(uri)
    try:
        db = client[db_name]
        results = db[collection].find().limit(limit)
        for r in results:
            pprint.pp(r)
    finally:
        client.close()

if __name__ == "__main__":
    app()