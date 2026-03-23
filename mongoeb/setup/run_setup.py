import json
import shutil
import getpass
from pathlib import Path
import rich

CONFIG_DIR = Path.home() / ".mongoeb"
CONFIG_FILE = CONFIG_DIR / "config.json"

# ------------------
# ENTRY POINT
# ------------------
def run_setup():
    """
    Run setup for Mongoeb.

    Prompts user. This is main entry point used by CLI.
    """
    if not confirm_overwrite():
        rich.print("[orange]Aborting setup.[/orange]")
        return

    rich.print("[bold]👋[/bold]  Howdy! First-time setup\n")
    CONFIG_DIR.mkdir(exist_ok=True)
    print(f"📁  Config directory: {CONFIG_DIR}\n")

    base_config = ask_for_config()
    tls_options = handle_tls()

    config = build_config(base_config, tls_options)
    save_config(config)

# ------------------
# USER INPuTS
# ------------------
def confirm_overwrite() -> bool:
    if not CONFIG_FILE.exists():
        return True

    confirm = input("Config already exists. Overwrite it? (y/n): ").strip().lower()
    return confirm in ("y", "yes")


def ask_for_config() -> dict[str, str | int]:

    def required(prompt: str) -> str:
        while True:
            value = input(prompt).strip()
            if value:
                return value
            print("This field is required.")

    def ask_port() -> int:
        while True:
            _port = input("Port: ").strip()
            if _port.isdigit():
                return int(_port)
            print("Invalid port. Please enter a number.")

    database = required("Database: ")
    username = required("Username: ")
    password = getpass.getpass("Password: ")
    host = required("Mongo host: ")
    port = ask_port()
    auth_source = required("Auth Source: ")

    return {
        "database": database,
        "username": username,
        "password": password,
        "host": host,
        "port": port,
        "auth_source": auth_source,
    }

# ------------------
# CONFIG BUILDING
# ------------------
def build_config(base: dict, options: dict) -> dict:
    full_options = {
        **options,
        "authSource": base["auth_source"]
    }

    return {
        "database": base["database"],
        "username": base["username"],
        "password": base["password"],
        "host": base["host"],
        "port": base["port"],
        "scheme": "mongodb",
        "options": full_options,
    }

# ------------------
# TLS HANDLING
# ------------------
def handle_tls() -> dict[str, str | bool] | None:
    """
    Handle TLS setup.

    if enabled:
    - Asks user for CA cert path.
    - Copies it into config dir.
    - returns TLS connection options
    """
    use_tls = input("\nUse TLS? (y/n): ").lower() == "y"
    if not use_tls:
        return {}

    rich.print("\n[bold]🔐  TLS setup required[/bold]\n")
    print("1. Download CA file from:")
    print("   https://truststore.pki.rds.amazonaws.com/global/global-bundle.pem\n")
    print("2. Save it somewhere")
    print("3. Paste full path to the file:\n")

    dest = (CONFIG_DIR / "global-bundle.pem").resolve()

    while True:
        user_path = input("> ").strip()
        src = Path(user_path).resolve()

        if not src.exists():
            print("File not found. Please try again.\n")
            continue

        if src != dest:
            shutil.copy(src, dest)
            print(f"\nSaved to: {dest}\n")
        else:
            print("Certificate already in correct location.\n")

        return {
            "retryWrites": "false",
            "tls": "true",
            "tlsCAFile": "global-bundle.pem",
            "tlsAllowInvalidHostnames": "true",
            "directConnection": "true",
        }

# ------------------
# PERSISTENCE
# ------------------
def save_config(config: dict):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)

    print("Setup complete!")
    rich.print(f"[bold]📄[/bold]  Config saved to: {CONFIG_FILE}")
