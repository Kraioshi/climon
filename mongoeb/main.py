import typer
from mongoeb.cli.commands import app as commands_app
from mongoeb.cli.visual.browsing import app as visual_app

app = typer.Typer(help="MongoDB exploration CLI")

# sub-apps
app.add_typer(commands_app)
app.add_typer(visual_app)


def main():
    app()


if __name__ == "__main__":
    main()
