from abc import abstractmethod
from types import TracebackType
from typing import Protocol


class QuerySession[SessionType](Protocol):

    @abstractmethod
    async def __aenter__(self) -> SessionType: ...

    @abstractmethod
    async def __aexit__(
        self,
        typ: type[BaseException] | None,
        value: BaseException | None,
        traceback: TracebackType | None,
    ) -> bool | None: ...


class QuerySessionManager[SessionType](Protocol):

    @abstractmethod
    def __call__(self) -> QuerySession[SessionType]: ...
