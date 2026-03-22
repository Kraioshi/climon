import re

import typer


class InputValidator:
    @staticmethod
    def validate_limit(limit: int, max_limit: int = 100):
        if limit > max_limit:
            raise typer.BadParameter("Limit is too high.")
        if limit <= 0:
            raise typer.BadParameter("Limit must be positive.")

    @staticmethod
    def validate_collection_name(collection: str):
        if not re.match(r'^[a-zA-Z0-9_\-]+$', collection):
            raise typer.BadParameter(f"Invalid collection name {collection}.")


    @staticmethod
    def validate_filters(filters: list[str] | None):
        if not filters:
            return

        for f in filters:
            if "=" not in f:
                raise ValueError(
                    f"Invalid filter '{f}'. Use key=value format (e.g. age=30)"
                )

            key, value = f.split("=", 1)

            if not key:
                raise ValueError(f"Empty filter key in '{f}'")

            if not value:
                raise ValueError(f"Empty filter value in '{f}'")

