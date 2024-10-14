from typing import Protocol

from app.modules.common.domain.msg_bus.msg import Message


class DomainEvent(Message, Protocol): ...
