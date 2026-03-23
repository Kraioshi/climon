import json
import shutil
from pathlib import Path

CONFIG_DIR = Path.home() / ".mongoeb"
CONFIG_FILE = CONFIG_DIR / "config.json"


def run_setup():
    print("Howdy! First-time setup\n")

    database = input("Database: ")
    username = input("Username: ")
    password = input("Password: ")
    host = input("Mongo host: ")
    port = input("Port: ")

    use_tls = input("\nUse TLS? (y/n): ").lower() == "y"

    options = {}

    CONFIG_DIR.mkdir(exist_ok=True)

    if use_tls:
        print("\n TLS setup required\n")
        print("1. Download CA file from:")
        print("   https://truststore.pki.rds.amazonaws.com/global/global-bundle.pem\n")
        print("2. Save it somewhere")
        print("3. Paste full path to the file:\n")

        while True:
            user_path = input("> ").strip()
            src = Path(user_path).resolve()
            dest = (CONFIG_DIR / "global-bundle.pem").resolve()

            if not src.exists():
                print("File not found. Please try again.\n")
                continue

            if src == dest:
                print("Certificate already in correct location. Skipping copy.\n")
            else:
                shutil.copy(src, dest)
                print(f"\n Saved to: {dest}\n")
            print(f"\n Saved to: {dest}\n")

            options = {
                "retryWrites": "false",
                "tls": "true",
                "tlsCAFile": "global-bundle.pem",
                "tlsAllowInvalidHostnames": "true",
                "directConnection": "true"
            }

            break

    auth_source = input("Auth Source: ")
    options["AuthSource"] = auth_source


    config = {
        "database": database,
        "username": username,
        "password": password,
        "host": host,
        "port": int(port),
        "scheme": "mongodb",
        "options": options
    }

    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)

    print("Setup complete!")
