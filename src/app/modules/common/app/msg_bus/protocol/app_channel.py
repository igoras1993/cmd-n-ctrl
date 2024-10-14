from abc import abstractmethod
from typing import Protocol, Sequence

from app.modules.common.app.msg_bus.protocol.listener import ListenerProtocol
from app.modules.common.domain.msg_bus.msg import Message
from app.modules.common.app.msg_bus.protocol.registration import (
    RegistrationProtocol,
)


class ApplicationChannelProtocol(Protocol):

    @abstractmethod
    def register[
        Msg: Message
    ](self, listener: ListenerProtocol[Msg], msg_type: type[Msg]) -> RegistrationProtocol[
        Msg
    ]:
        """
        Raises:
            [app.modules.common.application.message_bus.errors.RegistrationAlreadyExists][]
                If registration already exists in this channel
        """  # noqa
        ...

    @abstractmethod
    def get_registrations(self) -> Sequence[RegistrationProtocol[Message]]: ...

    @abstractmethod
    def get_listeners_for[
        Msg: Message
    ](self, msg: Msg) -> Sequence[ListenerProtocol[Msg]]: ...
