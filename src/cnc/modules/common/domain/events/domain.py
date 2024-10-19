from typing import Protocol

from cnc.modules.common.domain.msg_bus.msg import Message


class DomainEvent(Message, Protocol): ...
