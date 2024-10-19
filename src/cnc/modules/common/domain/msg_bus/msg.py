from typing import Protocol


class Message(Protocol):
    def __hash__(self) -> int: ...
