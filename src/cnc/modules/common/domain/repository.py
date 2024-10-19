from typing import Any, Protocol, Sequence
from abc import abstractmethod
from uuid import UUID
from cnc.modules.common.domain.entity import Entity


class Repository(Protocol):
    """
    Abstraction for data storage
    """

    @abstractmethod
    def add(self, entity: Entity) -> None: ...

    @abstractmethod
    async def flush(self, entities: Sequence[Entity] | None, **kwargs: Any) -> None: ...

    @abstractmethod
    async def get[
        T: Entity
    ](self, entity_type: type[T], key: UUID, **kwargs: Any) -> T: ...

    @abstractmethod
    async def delete(self, entity: Entity, **kwargs: Any) -> None: ...
