import typer
from pyvis.network import Network

from mongoeb.core.db import get_db
from mongoeb.core.services.helpers import show_docs
from mongoeb.core.validators import InputValidator
from mongoeb.core.visualize.field_extraction import extract_fields

from mongoeb.core.graph.build_graph import build_graph

app = typer.Typer()
validator = InputValidator()


@app.command("graph")
def graph(
    collection: str,
    limit: int = typer.Option(20, "--limit")
):
    """
    Generate graph visualization of a collection schema.

    This command analyzes sample of documents and build a graph representing structure + nesting
    Each top level field is connected to the collection root, nested fields are displayed hierarchically.

    Result is rendered as an interactive HTML file using pyvis.

    Usage:
        mongoeb graph collection
    :param collection: Name of mongoDB collection.
    :param limit: sample size
    """
    net = Network('960px', '100%', bgcolor="#222222", font_color="white")
    field_map: dict = {}
    with get_db() as db:
        docs = show_docs(db=db, collection=collection, limit=limit)

    for doc in docs:
        extract_fields(doc, field_map)
    build_graph(net, collection=collection, field_map=field_map)

    net.toggle_physics(True)
    net.show(f"{collection}.html", notebook=False)
