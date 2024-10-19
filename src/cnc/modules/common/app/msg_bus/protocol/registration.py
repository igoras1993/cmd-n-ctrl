from abc import abstractmethod
from typing import Protocol
from cnc.modules.common.app.msg_bus.protocol.listener import ListenerProtocol
from cnc.modules.common.domain.msg_bus.msg import Message


class RegistrationProtocol[Msg: Message](Protocol):

    @property
    @abstractmethod
    def listener(self) -> ListenerProtocol[Msg]: ...

    @property
    @abstractmethod
    def msg_type(self) -> type[Msg]: ...
