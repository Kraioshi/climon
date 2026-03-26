def build_html_list(data: list[str]) -> str:
    items = ''.join(f"<li>{entry}</li>" for entry in data)

    content = f"""
    <h2>Collections</h2>
    <ul>
        {items}
    </ul>
    """
    return wrap_html(content)

def build_html_collection_table(data: list[str]) -> str:
    rows = ''.join(f"<tr><td>{entry}</td></tr>" for entry in data)

    content = f"""
    <table>
        <tr>
            <th>Collections</th>
        </tr>
        {rows}
    </table>
    """

    return wrap_html(content)

def build_html_count_table(data: dict[str, int]) -> str:
    rows = ''.join(
        f"<tr><td>{collection}</td><td>{count}</td></tr>"
        for collection, count in data.items()
    )

    content = f"""
    <table>
        <tr>
            <th>Collections</th>
            <th>Count</th>
        </tr>
        {rows}
    </table>
    """

    return wrap_html(content)


def wrap_html(content: str) -> str:
    return f"""
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
            {content}
        </body>
    </html>
    """