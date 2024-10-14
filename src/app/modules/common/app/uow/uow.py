from abc import abstractmethod
from contextlib import AbstractAsyncContextManager
from typing import Any, Protocol

from app.modules.common.app.uow.enum import WorkloadStrategy
from app.modules.common.domain.msg_bus.msg import Message
from app.modules.common.domain.repository import Repository


# I see that some wise heads are placing UoW in domain layer
# However I am finding it unnecessary
# https://github.com/dotnet-architecture/eShopOnContainers/issues/923


class UnitOfWork(Protocol):
    """
    Abstraction for operation atomicity
    """

    @abstractmethod
    def get_repository(self) -> Repository: ...

    @abstractmethod
    async def push(self, msg: Message, workload_strategy: WorkloadStrategy) -> Any: ...

    @abstractmethod
    async def commit(self, **kwargs: Any) -> Any: ...

    @abstractmethod
    async def rollback(self, **kwargs: Any) -> Any: ...

    @abstractmethod
    def start(self) -> AbstractAsyncContextManager[Any]: ...
