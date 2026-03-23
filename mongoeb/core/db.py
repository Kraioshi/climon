from contextlib import contextmanager
from pathlib import Path

from pymongo import MongoClient

from mongoeb.config_file import CONFIG_DIR
from mongoeb.core.config import load_config
from mongoeb.core.uri import build_uri


@contextmanager
def get_db():
    config = load_config()
    uri = build_uri(config)

    params = config.options or {}

    tls = to_bool(params.get("tls"))
    tls_ca_file = resolve_ca_pem(params.get("tlsCAFile"))
    direct_connection = to_bool(params.get("directConnection"))

    client = MongoClient(
        uri,
        tls=tls,
        tlsCAFile=tls_ca_file,
        directConnection=direct_connection,
    )

    try:
        db = client[config.database]
        yield db
    finally:
        client.close()


def resolve_ca_pem(path: str | None) -> str | None:
    if not path:
        return None

    p = Path(path)

    if not p.is_absolute():
        p = (CONFIG_DIR / path).resolve()

    if not p.exists():
        raise FileNotFoundError(
            f"TLS CA file not found: {p}\n"
            "Run 'mongoeb gazuyem' to configure TLS properly."
        )

    return str(p)


def to_bool(val: str | None) -> bool:
    return str(val).lower() == "true"
