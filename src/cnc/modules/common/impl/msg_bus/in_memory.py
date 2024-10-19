from typing import Sequence
from cnc.modules.common.app.msg_bus.app_channel import ApplicationChannel
from cnc.modules.common.app.msg_bus.protocol.app_channel import (
    ApplicationChannelProtocol,
)
from cnc.modules.common.app.msg_bus.protocol.bus import MessageBus
from cnc.modules.common.domain.msg_bus.msg import Message
from cnc.shared.logging import get_logger

logger = get_logger(__name__)


class InMemoryMessageBus(MessageBus):
    """
    This message bus implementation dispatches messages immediately after it is
    received.

    Raises:
        [app.modules.common.application.message_bus.errors.RegistrationAlreadyExists][]
            If registration already exists in this channel

    """  # noqa

    def __init__(
        self, channels: Sequence[ApplicationChannelProtocol] | None = None
    ) -> None:
        self._channels: list[ApplicationChannelProtocol] = []

        # Stores registration map unpacked from all mounted channels
        self._bus_channel = ApplicationChannel()

        for channel in channels or []:
            self.mount(channel)

    def mount(self, channel: ApplicationChannelProtocol) -> None:
        """
        Raises:
            [app.modules.common.application.message_bus.errors.RegistrationAlreadyExists][]
                If registration already exists in this channel
        """  # noqa
        # Unpack channel into bus channel
        for registration in channel.get_registrations():
            self._bus_channel.register(
                listener=registration.listener, msg_type=registration.msg_type
            )

        self._channels.append(channel)

    async def dispatch(self, msg: Message) -> None:

        listener = None
        for listener in self._bus_channel.get_listeners_for(msg):
            await listener(msg)

        if listener is None:
            # No listeners for this message
            logger.warning("No listeners found for %s. Dispatcher did no work.", msg)
