from abc import abstractmethod
from typing import Protocol
from app.modules.common.app.msg_bus.protocol.listener import ListenerProtocol
from app.modules.common.domain.msg_bus.msg import Message


class RegistrationProtocol[Msg: Message](Protocol):

    @property
    @abstractmethod
    def listener(self) -> ListenerProtocol[Msg]: ...

    @property
    @abstractmethod
    def msg_type(self) -> type[Msg]: ...
