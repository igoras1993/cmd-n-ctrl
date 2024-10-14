from collections import defaultdict
from typing import Callable, Sequence

from app.modules.common.app.msg_bus.errors import RegistrationAlreadyExists
from app.modules.common.app.msg_bus.protocol.app_channel import (
    ApplicationChannelProtocol,
)
from app.modules.common.app.msg_bus.protocol.listener import ListenerProtocol
from app.modules.common.domain.msg_bus.msg import Message
from app.modules.common.app.msg_bus.registration import Registration


class ApplicationChannel(ApplicationChannelProtocol):

    def __init__(self) -> None:
        self._reg_map: dict[type[Message], list[Registration]] = defaultdict(list)

    def register[
        Msg: Message
    ](self, listener: ListenerProtocol[Msg], msg_type: type[Msg]) -> Registration[Msg]:
        """
        Raises:
            [app.modules.common.application.message_bus.errors.RegistrationAlreadyExists][]
                If registration already exists in this channel
        """  # noqa
        reg = Registration(listener, msg_type)
        reg_store = self._reg_map[msg_type]
        if reg in reg_store:
            raise RegistrationAlreadyExists(
                f"Registration {reg} already present in this channel"
            )
        self._reg_map[msg_type].append(reg)
        return reg

    def get_registrations(self) -> Sequence[Registration[Message]]:
        return [reg for reg_list in self._reg_map.values() for reg in reg_list]

    def get_listeners_for[
        Msg: Message
    ](self, msg: Msg) -> Sequence[ListenerProtocol[Msg]]:
        return [reg.listener for reg in self._reg_map[type(msg)]]

    def listen_for[
        Msg: Message
    ](self, msg_type: type[Msg]) -> Callable[
        [ListenerProtocol[Msg]], ListenerProtocol[Msg]
    ]:
        def decorator(listener: ListenerProtocol[Msg], /) -> ListenerProtocol[Msg]:
            self.register(listener, msg_type)
            return listener

        return decorator
