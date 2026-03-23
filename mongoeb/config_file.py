from pathlib import Path
import json

CONFIG_DIR = Path.home() / ".mongoeb"
CONFIG_FILE = CONFIG_DIR / "config.json"


def config_exist() -> bool:
    return CONFIG_FILE.exists()


def load_config_file() -> dict:
    if not config_exist():
        return {}

    with open(CONFIG_FILE) as f:
        return json.load(f)
