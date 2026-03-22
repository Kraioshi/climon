from textwrap import dedent

import rich
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.json import JSON
from rich.text import Text
import json

from bson import ObjectId
import datetime

console = Console(force_terminal=True)


def print_output(
        docs: list[dict],
        output_format: str | None = None,
        collection: str | None = None,
) -> None:
    match output_format:
        case "table":
            if not collection:
                raise ValueError("Collection is required for table format")
            print_table(docs, collection)
        case "compact":
            print_compact(docs)
        case "pretty":
            print_json(docs)
        case _:
            print_json(docs)


def print_table(docs, collection: str):
    if not docs:
        print("No documents found.")
        return

    table = Table(title=collection, expand=True)

    columns = list(docs[0].keys())
    if "_id" in columns:
        columns.remove("_id")
        columns.insert(0, "_id")
    for col in columns:
        table.add_column(col, header_style='yellow')

    for doc in docs:
        row = []
        for col in columns:
            value = doc.get(col, "")
            row.append(str(value))
        table.add_row(*row)

    console.print(table)


def print_json(docs):
    if not docs:
        print("No documents found.")
        return

    for doc in docs:
        safe_doc = normalize(doc)
        json_str = json.dumps(safe_doc, indent=2)
        console.print(JSON(json_str))


def print_compact(docs: list[dict]) -> None:
    if not docs:
        print("No documents found.")
        return

    for doc in docs:
        line = Text()

        for key, value in doc.items():
            formatted = _format_value(value)

            line.append(key, style="yellow")
            line.append("=")
            line.append(formatted)
            line.append(" ")
        line.append("\n")

        console.print(line)


def print_shell_help():
    content = """
[bold yellow]Mongoeb Interactive Shell[/bold yellow]

[bold]Commands:[/bold]
  show <collection>
  show-collections
  count <collection>
  find <collection> (filters)

[bold]Find modifiers:[/bold]
  include <fields>     Include only specific fields
  exclude <fields>     Exclude fields
  limit <number>       Limit results
  one                  Return single document

[bold]Examples:[/bold]
    show employees
    count employees
    find benefit benefit_id=abc123 name="Free Will"
    find benefit benefit_id=abc123 | include name description | limit 5

[bold]Other:[/bold]
  help                          Show help
  zaebal / exit / quit          Exit shell
    """

    rich.print(
        Panel.fit(
            content,
            title="[bold yellow]Mongoeb Shell[/bold yellow]",
            border_style="cyan"
        )
    )


def normalize(value):
    if isinstance(value, ObjectId):
        return str(value)
    if isinstance(value, datetime.datetime):
        return value.isoformat()
    if isinstance(value, dict):
        return {k: normalize(v) for k, v in value.items()}
    if isinstance(value, list):
        return [normalize(v) for v in value]

    return value


def _format_value(value, max_length: int = 40) -> str:
    value = normalize(value)

    if isinstance(value, (dict, list)):
        value = json.dumps(value, separators=(",", ":"))

    value_str = str(value)

    if len(value_str) > max_length:
        return value_str[: max_length - 3] + "..."
    return value_str
