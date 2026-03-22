import shlex

import rich

from mongoeb.core.printer import print_output, print_shell_help
from mongoeb.core.db import get_db
from mongoeb.shell.command_executor import handle_commands


def shell():
    """Interactive shell loop for Mongoeb."""
    with get_db() as db:
        while True:
            try:
                cmd = input("mongoeb > ")

                if cmd in ["help", "pomomongo"]:
                    print_shell_help()
                    continue

                if cmd in ["exit", "quit", "zaebal"]:
                    break

                # Temporary naive parsing
                parts = shlex.split(cmd)
                # print(parts)
                if not parts:
                    continue

                result = handle_commands(db, parts)

                command = parts[0]
                if command == "count":
                    collection = parts[1]
                    rich.print(f"{collection} count: {result}")
                elif command == "show-collections":
                    print_output(docs=result, collection="collections")

                elif command in ["show", "find"]:
                    collection = parts[1]
                    print_output(result, collection)
                else:
                    print_output(result, collection)

            except Exception as e:
                rich.print(f"[red]Error:[/red] {e}")
                rich.print(f"[orange]Type 'help' or 'pomomongo' to see available commands[/orange]")
