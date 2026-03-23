import typer
from mongoeb.cli.commands import app as commands_app



app = typer.Typer(help="MongoDB exploration CLI")
app.add_typer(commands_app)


def main():
    app()


if __name__ == "__main__":
    main()
