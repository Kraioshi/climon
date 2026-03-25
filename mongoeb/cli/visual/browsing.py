import webbrowser
from pathlib import Path

import rich
import typer

from mongoeb.core.db import get_db
from mongoeb.core.validators import InputValidator

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
        case _:
            rich.print("Unknown command")


def visualize_all():
    file = Path(TMP_DIR) / "mongoeb-collections.html"

    with get_db() as db:
        results = sorted(list(db.list_collection_names()))

    html = _build_html(results)
    file.write_text(html, encoding="UTF-8")
    rich.print(f"[bold]📄[/bold]  File saved as: [gold3]{file}[/gold3]")

    webbrowser.open(file.as_uri())

def visualize_table():
    file = Path(TMP_DIR) / "mongoeb-collections-table.html"

    with get_db() as db:
        results = sorted(list(db.list_collection_names()))

    html = _build_html_table(results)
    file.write_text(html, encoding="UTF-8")
    rich.print(f"[bold]📄[/bold]  File saved as: [gold3]{file}[/gold3]")

    webbrowser.open(file.as_uri())

def _create_temp_folder():
    if not TMP_DIR.exists():
        TMP_DIR.mkdir(exist_ok=True)
        rich.print(f"[bold]📁[/bold]  Creating temp directory: [gold3]{TMP_DIR}[/gold3]\n")

def _build_html(data: list[str]) -> str:
    items = ''.join(f"<li>{entry}</li>" for entry in data)

    html_str = f"""
    <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    padding: 20px;
                }}

                h2 {{
                    margin-bottom: 10px;
                }}

                ul {{
                    list-style: none;
                    padding: 0;
                    margin: 0;
                    width: 300px;
                    border: 1px solid #ddd;
                    border-radius: 6px;
                    overflow: hidden;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                }}

                li {{
                    padding: 10px;
                    border-bottom: 1px solid #eee;
                    cursor: pointer;
                }}

                li:last-child {{
                    border-bottom: none;
                }}

                li:hover {{
                    background-color: #f1f1f1;
                }}
            </style>
        </head>
        <body>
            <h2>Collections</h2>
            <ul>
                {items}
            </ul>
        </body>
    </html>
    """
    return html_str

def _build_html_table(data: list[str]) -> str:
    rows = ''.join(f"<tr><td>{entry}</td></tr>" for entry in data)
    html_str = f"""
        <html>
            <head>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        padding: 20px;
                    }}
                    table {{
                        border-collapse: collapse;
                        width: 300px;
                        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                        border-radius: 6px;
                        overflow: hidden;
                    }}
                    th, td {{
                        border: 1px solid #ddd;
                        padding: 8px;
                    }}
                    th {{
                        background-color: #f4f4f4;
                        text-align: left;
                    }}
                    tr:hover {{
                        background-color: #f1f1f1;
                    }}
                </style>
            </head>
            <body>
                <table>
                    <tr>
                        <th>Collections</th>
                    </tr>
                    {rows}
                </table>
            </body>
        </html>
    """
    return html_str
