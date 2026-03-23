import os
from dataclasses import dataclass

from mongoeb.config_file import load_config_file


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

    file_config = load_config_file()

    config = Config(
        database=get_value("M_DATABASE", "database", file_config),
        username=get_value("M_USERNAME", "username", file_config),
        password=get_value("M_PASSWORD", "password", file_config),
        host=get_value("M_HOST", "host", file_config),
        port=int(get_value("M_PORT", "port", file_config)),
        scheme=get_value("M_SCHEME", "scheme", file_config),
    )
    config.validate()
    return config

def get_value(env_key: str, file_key: str, file_config: dict):
    return os.getenv(env_key) or file_config.get(file_key)