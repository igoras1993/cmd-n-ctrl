from abc import ABC
from uuid import UUID
from app.modules.common.domain.entity import Entity


class DomainException(Exception, ABC):
    pass


class ObjectNotFound(DomainException):
    def __init__(self, msg: str, model: type[Entity], id: UUID):
        self.id = id
        self.model = model
        super().__init__(msg)
