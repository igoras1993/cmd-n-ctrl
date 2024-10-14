from abc import abstractmethod
from typing import Callable, Protocol


class InstancePropertyImplProtocol[Instance, Value](Protocol):
    setter: Callable[[Instance, Value], None] | None
    deleter: Callable[[Instance], None] | None

    @abstractmethod
    def getter(self, inst: Instance) -> Value: ...
