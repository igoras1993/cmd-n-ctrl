from collections import deque
from dataclasses import dataclass, field
from uuid import UUID, uuid4

from cnc.modules.common.domain.msg_bus.msg import Message


@dataclass
class CtxData:
    id: UUID = field(default_factory=uuid4)
    deferred_messages: deque[Message] = field(default_factory=deque)
