from abc import abstractmethod
from typing import Any, Protocol

from app.modules.common.app.msg_bus.protocol.app_channel import (
    ApplicationChannelProtocol,
)
from app.modules.common.domain.msg_bus.msg import Message


class MessageBus(Protocol):

    @abstractmethod
    def mount(self, channel: ApplicationChannelProtocol) -> Any: ...

    @abstractmethod
    async def dispatch(self, msg: Message) -> Any: ...
