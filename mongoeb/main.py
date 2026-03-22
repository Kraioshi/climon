import os

import typer
from dotenv import load_dotenv
from mongoeb.cli.commands import app as commands_app



app = typer.Typer(help="MongoDB exploration CLI")
app.add_typer(commands_app)


def main():
    load_dotenv()

    if not os.getenv("MONGO_URI"):
        typer.echo("Error: MONGO_URI not set")
        raise typer.Exit(code=1)

    app()


if __name__ == "__main__":
    main()
