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
