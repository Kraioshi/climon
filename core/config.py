import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Config:
    database: str
    username: str
    password: str
    host: str
    port: int
    scheme: str

    def validate(self):
        missing = [
            name for name, value in self.__dict__.items() if value is None or value == ""
        ]
        if missing:
            raise RuntimeError(f"Missing env vars: {', '.join(missing)}")


def load_config() -> Config:
    config = Config(
        database=os.getenv("M_DATABASE"),
        username=os.getenv("M_USERNAME"),
        password=os.getenv("M_PASSWORD"),
        host=os.getenv("M_HOST"),
        port=int(os.getenv("M_PORT")),
        scheme=os.getenv("M_SCHEME"),
    )
    config.validate()
    return config
