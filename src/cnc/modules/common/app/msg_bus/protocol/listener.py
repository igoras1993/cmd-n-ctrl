from abc import abstractmethod
from typing import Any, Protocol
from cnc.modules.common.domain.msg_bus.msg import Message


class ListenerProtocol[Msg: Message](Protocol):

    @abstractmethod
    async def __call__(self, msg: Msg) -> Any: ...
