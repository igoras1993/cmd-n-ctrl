from app.modules.common.impl.tools.http.client_reg import SharedHttpClientRegistry


def provide_http_client_reg() -> SharedHttpClientRegistry:
    return SharedHttpClientRegistry(
        default_client_kwargs={"timeout": 15}
    )  # Timeout in seconds
