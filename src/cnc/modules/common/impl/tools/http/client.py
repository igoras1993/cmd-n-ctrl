import typing as t
import asyncio
from dataclasses import dataclass
from httpx import AsyncClient


@dataclass(frozen=True)
class SupplyDescription:
    resource_id: t.Hashable


class SharedHttpClient:
    """
    The interface for concurrently handling http calls utilizing one connection.
    It is coroutine safe, and designed to work in singleton-like manner.
    Instantiate it once, use everywhere.
    """

    def __init__(self, *, base_url: str, **client_kwargs: t.Any):
        self.base_url = base_url
        self._client = None

        self._client_kwargs = client_kwargs
        self._shared_lock = asyncio.Lock()
        self._shared_api_count = 0

    def create_client(self, force: bool = False) -> None:
        """
        Creates the client manually, without usage of context manager. Remember to call
        `.close_client()` after finish. If client already exists, no new client is
        spawned, unless ``force=True`` is passed.

        Args:
            force: force spawning new client instead utilizing existing one. It replaces
                further usages with this new one.
        """
        if force or self._client is None:
            self._client = AsyncClient(
                base_url=self.base_url, **self._client_kwargs
            )  # TODO: make a timeout configurable.

    async def close_client(self) -> None:
        """
        Closes the connection for the existing client. If client does not exists, it
        raises ``RuntimeError``.
        """
        await self.client.aclose()
        self._client = None

    @property
    def client(self) -> AsyncClient:
        """
        Returns async client.
        """
        if self._client is None:
            raise RuntimeError(  # pragma: no cover
                f"No client available on {self}. You must ensure context when"
                " dealing with requests."
            )

        return self._client

    async def __aenter__(self):
        """
        Establishes context for new client usage.
        """
        assert self._shared_api_count >= 0

        async with self._shared_lock:
            self._shared_api_count += 1
            self.create_client()

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        async with self._shared_lock:
            self._shared_api_count -= 1
            if self._shared_api_count <= 0:
                await self.close_client()

        assert self._shared_api_count >= 0
        return False
