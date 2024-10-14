import typing as t
from .client import SharedHttpClient


class SharedHttpClientRegistry:
    """
    Registry for storing and retrieving [.SharedHttpClient] instances.
    """

    def __init__(self, default_client_kwargs: dict[str, t.Any] | None = None) -> None:
        self._reg: dict[str, SharedHttpClient] = dict()
        self._default_client_kwargs: dict[str, t.Any] = (
            default_client_kwargs if default_client_kwargs is not None else dict()
        )

    def truncate_base_url(self, url: str) -> str:
        """
        Removes '/' suffixes from given url.

        Args:
            url: URL to be truncated

        Returns:
            Truncated URL
        """
        return url.rstrip("/")

    def get_standalone(
        self, base_url: str, client_kwargs: dict[str, t.Any] | None = None
    ) -> SharedHttpClient:
        """
        Creates [.SharedHttpClient] instance but does not registers it.

        Args:
            base_url: Base URL for new client
            client_kwargs: Optional additional arguments for creating a client. If not
                given, then the `default_client_kwargs` are used.

        Returns:
            New [.SharedHttpClient] instance.

        """
        use_base_url = self.truncate_base_url(base_url)
        use_client_kwargs: dict[str, t.Any] = (
            client_kwargs if client_kwargs is not None else self._default_client_kwargs
        )

        return SharedHttpClient(base_url=use_base_url, **use_client_kwargs)

    def register(
        self, base_url: str, client_kwargs: dict[str, t.Any] | None = None
    ) -> SharedHttpClient:
        """
        Creates new client instance in registry. Raises `KeyError` if given base URL is
        already registered.

        Args:
            base_url: Base URL for new client
            client_kwargs: Optional additional arguments for creating a client. If not
                given, then the default_client_kwargs are used.

        Returns:
            Newly registered [.SharedHttpClient] instance.

        """
        use_base_url = self.truncate_base_url(base_url)

        if use_base_url in self._reg:
            raise KeyError(f"{use_base_url} is already registered")

        client = self.get_standalone(use_base_url, client_kwargs)

        self._reg[use_base_url] = client

        return client

    def get(self, base_url: str) -> SharedHttpClient:
        """
        Returns already registered client. If given base_url is not yet registered,
        registers it with default arguments.

        Args:
            base_url: base URL to be looked up in registry

        Returns:
            Registered instance of [.SharedHttpClient]

        """
        use_base_url = self.truncate_base_url(base_url)

        try:
            client = self._reg[use_base_url]
        except KeyError:
            client = self.register(base_url=use_base_url)

        return client
