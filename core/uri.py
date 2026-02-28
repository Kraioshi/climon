from urllib.parse import urlencode

from core.params import  get_query_params
from core.config import Config


def build_uri(config: Config) -> str:
    base = (f"{config.scheme}://"
            f"{config.username}:{config.password}"
            f"@{config.host}:{config.port}/{config.database}")
    params = get_query_params()
    if params:
        return f"{base}?{urlencode(params)}"
    return base


