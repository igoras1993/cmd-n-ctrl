from typing import Any, Sequence
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.common.domain.entity import Entity
from app.modules.common.domain.exception.base import ObjectNotFound
from app.modules.common.domain.repository import Repository


class SqlAlchemyRepository(Repository):

    def __init__(self, session: AsyncSession):
        self._session = session

    def add(self, entity: Entity) -> None:
        self._session.add(entity)

    async def flush(self, entities: Sequence[Entity] | None, **kwargs: Any) -> None:
        await self._session.flush(entities)

    async def get[T: Entity](self, entity_type: type[T], key: UUID, **kwargs: Any) -> T:
        entity = await self._session.get(entity_type, key, with_for_update=True, **kwargs)

        if entity is None:
            raise ObjectNotFound("Entity not found", entity_type, key)

        return entity

    async def delete(self, entity: Entity, **kwargs: Any) -> None:
        await self._session.delete(entity)
