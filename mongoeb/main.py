import typer
from mongoeb.cli.commands import app as commands_app
from mongoeb.cli.visualize.browsing import app as visual_app
from mongoeb.cli.graph.graph_commands import app as graph_app

app = typer.Typer(help="MongoDB exploration CLI")

# sub-apps
app.add_typer(commands_app)
app.add_typer(visual_app)
app.add_typer(graph_app)


def main():
    app()


if __name__ == "__main__":
    main()
