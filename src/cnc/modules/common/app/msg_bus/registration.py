from dataclasses import dataclass
from cnc.modules.common.app.msg_bus.protocol.listener import ListenerProtocol
from cnc.modules.common.app.msg_bus.protocol.registration import (
    RegistrationProtocol,
)
from cnc.modules.common.domain.msg_bus.msg import Message


@dataclass(frozen=True)
class Registration[Msg: Message](RegistrationProtocol):
    _listener: ListenerProtocol[Msg]
    _msg_type: type[Msg]

    @property
    def listener(self) -> ListenerProtocol[Msg]:
        return self._listener

    @property
    def msg_type(self) -> type[Msg]:
        return self._msg_type

    def __eq__(self, value: object) -> bool:
        try:
            other_listener = getattr(value, "listener")
        except AttributeError:
            return False

        try:
            other_msg_type = getattr(value, "msg_type")
        except AttributeError:
            return False

        return other_listener is self.listener and other_msg_type is self.msg_type
