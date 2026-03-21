from contextlib import contextmanager
from pymongo import MongoClient

from mongoeb.core.config import load_config
from mongoeb.core.uri import build_uri


@contextmanager
def get_db():
    config = load_config()
    uri = build_uri(config)
    client = MongoClient(uri)

    try:
        db = client[config.database]
        yield db
    finally:
        client.close()
