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
def graph(collection: str):
    net = Network('960px', '100%', bgcolor="#222222", font_color="white")
    field_map: dict = {}
    with get_db() as db:
        docs = show_docs(db=db, collection=collection, limit=20)

    for doc in docs:
        extract_fields(doc, field_map)
    build_graph(net, collection=collection, field_map=field_map)

    net.toggle_physics(True)
    net.show(f"{collection}.html", notebook=False)
