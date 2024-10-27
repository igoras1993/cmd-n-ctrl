from abc import abstractmethod
from typing import Protocol

from cnc.modules.common.domain.value_obj.memory import MemoryUsage


class ResourceConsumer(Protocol):
    """
    Protocol and ABC for all resource consumers
    """

    @abstractmethod
    def get_cpu_usage(self) -> float: ...

    @abstractmethod
    def get_memory_usage(self) -> MemoryUsage: ...
