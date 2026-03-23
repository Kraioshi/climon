from mongoeb.core.config import Config


def get_query_params(config: Config) -> dict:
    return {k: v for k, v in config.options.items() if v is not None}
