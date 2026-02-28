import os


def get_query_params() -> dict:
    query_params = {
        "retryWrites": os.getenv("M_RETRY_WRITES"),
        "tls": os.getenv("M_TLS"),
        "tlsCAFile": os.getenv("M_TLS_CA_FILE"),
        "tlsAllowInvalidHostnames": os.getenv("M_TLS_ALLOW_INVALID_HOSTNAMES"),
        "authSource": os.getenv("M_AUTH_SOURCE"),
        "directConnection": os.getenv("M_DIRECT_CONNECTION"),
    }

    filtered_params = {k: v for k, v in query_params.items() if v is not None}
    return filtered_params