from dotenv import load_dotenv
from mongoeb.cli.commands import app

load_dotenv()


def main():
    load_dotenv()
    app()


if __name__ == "__main__":
    main()
