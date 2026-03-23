import os
from dataclasses import dataclass, field

from mongoeb.config_file import load_config_file, CONFIG_FILE

@dataclass(frozen=True)
class Config:
    database: str
    username: str
    password: str
    host: str
    port: int
    scheme: str
    options: dict = field(default_factory=dict)

    def validate(self):
        missing = [
            name for name, value in self.__dict__.items() if value is None or value == ""
        ]
        if missing:
            raise RuntimeError(f"Missing env vars: {', '.join(missing)}")


def load_config() -> Config:

    file_config = load_config_file()
    values = {
        "database": get_value("M_DATABASE", "database", file_config),
        "username": get_value("M_USERNAME", "username", file_config),
        "password": get_value("M_PASSWORD", "password", file_config),
        "host": get_value("M_HOST", "host", file_config),
        "scheme": get_value("M_SCHEME", "scheme", file_config),
    }

    port_value = get_value("M_PORT", "port", file_config)
    values["port"] = int(port_value) if port_value is not None else None

    config = Config(
        **values,
        options=file_config.get("options", {})
    )
    config.validate()
    return config


def get_value(env_key: str, file_key: str, file_config: dict):
    env_val = os.getenv(env_key)
    file_val = file_config.get(file_key)

    if env_val is not None:
        return env_val
    if file_val is not None:
        return file_val
    else:
        return None

