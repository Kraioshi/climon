import webbrowser
from pathlib import Path

import rich
import typer

from mongoeb.core.db import get_db
from mongoeb.core.services.helpers import count_docs, show_docs
from mongoeb.core.validators import InputValidator
from mongoeb.core.visualize.html_builders import build_html_list, build_html_count_table, build_html_collection_table, \
    build_html_field_table

app = typer.Typer()
validator = InputValidator()

CONFIG_DIR = Path.home() / ".mongoeb"
TMP_DIR = CONFIG_DIR / "tmp"


@app.command("visualize")
def visualize(target: str):
    _create_temp_folder()
    match target:
        case "all":
            visualize_all()
        case "table":
            visualize_table()
        case "count":
            visualize_count()
        case _:
            rich.print("Unknown command")


def visualize_all():
    file = Path(TMP_DIR) / "mongoeb-collections.html"

    with get_db() as db:
        results = sorted(list(db.list_collection_names()))

    html = build_html_list(results)
    file.write_text(html, encoding="UTF-8")
    rich.print(f"[bold]📄[/bold]  File saved as: [gold3]{file}[/gold3]")

    webbrowser.open(file.as_uri())

def visualize_table():
    file = Path(TMP_DIR) / "mongoeb-collections-table.html"

    with get_db() as db:
        results = sorted(list(db.list_collection_names()))

    html = build_html_collection_table(results)
    file.write_text(html, encoding="UTF-8")
    rich.print(f"[bold]📄[/bold]  File saved as: [gold3]{file}[/gold3]")

    webbrowser.open(file.as_uri())

def visualize_count():
    file = Path(TMP_DIR) / "mongoeb-collections-count.html"

    doc_map: dict[str, int] = {}

    with get_db() as db:
        results = sorted(list(db.list_collection_names()))

        for entry in results:
            count = count_docs(db=db, collection=entry)
            doc_map[entry] = count

    html = build_html_count_table(doc_map)
    file.write_text(html, encoding="UTF-8")
    rich.print(f"[bold]📄[/bold]  File saved as: [gold3]{file}[/gold3]")

    webbrowser.open(file.as_uri())

@app.command("visualize-collection")
def visualize_fields(
        collection: str,
        sample_size: int = typer.Option(3, "--sample-size"),
) -> None:
    _create_temp_folder()
    html_name = f"mongoeb-{collection}-fields.html"
    file = Path(TMP_DIR) / html_name

    field_map: dict[str, int] = {}
    validator.validate_collection_name(collection)
    validator.validate_limit(sample_size)
    with get_db() as db:
        docs = show_docs(db=db, collection=collection, limit=sample_size)

    for doc in docs:
        _extract_fields(doc, field_map)


    html = build_html_field_table(data=field_map, collection=collection, sample_size=sample_size)
    file.write_text(html, encoding="UTF-8")
    rich.print(f"[bold]📄[/bold]  File saved as: [gold3]{file}[/gold3]")

    webbrowser.open(file.as_uri())


def _create_temp_folder():
    if not TMP_DIR.exists():
        TMP_DIR.mkdir(exist_ok=True)
        rich.print(f"[bold]📁[/bold]  Creating temp directory: [gold3]{TMP_DIR}[/gold3]\n")


def _extract_fields(doc: dict, field_map: dict[str, int], prefix: str = "") -> None:
    for key, value in doc.items():

        field_name = f"{prefix}.{key}" if prefix else key

        field_map[field_name] = field_map.get(field_name, 0) + 1

        if isinstance(value, dict):
            _extract_fields(value, field_map, field_name)

        if isinstance(value, list):
            array_field = f"{field_name}[]"
            field_map[array_field] = field_map.get(array_field, 0) + 1

            if value and isinstance(value[0], dict):
                _extract_fields(value[0], field_map, array_field)
