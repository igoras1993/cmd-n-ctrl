from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import Callable

from sqlalchemy.ext.asyncio import AsyncSession

from cnc.modules.common.app.service.query_session import (
    QuerySessionManager,
)


@dataclass
class SqlalchemySessionManager(QuerySessionManager[AsyncSession]):
    preferred_sessionmaker: Callable[[], AsyncSession]
    is_standalone: bool

    @asynccontextmanager
    async def __call__(self) -> AsyncGenerator[AsyncSession, None]:
        """
        Query sessions are always nested transactions that are rolled back at the end.
        """
        session = self.preferred_sessionmaker()

        if self.is_standalone:
            # Manage state
            async with session:
                yield session
        else:
            # Outer context manages
            yield session
