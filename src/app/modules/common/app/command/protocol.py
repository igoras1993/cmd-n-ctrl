from abc import abstractmethod
from typing import Protocol

from app.modules.common.app.uow.enum import WorkloadStrategy
from app.modules.common.domain.events.domain import DomainEvent


class WorkloadMapper(Protocol):
    """
    Abstract protocol for any workload mapper. Used by
    [app.modules.common.application.command.command.Command][]
    for simplifying event management.
    """

    @abstractmethod
    def get_event_workload(self, event: DomainEvent) -> WorkloadStrategy:
        """
        Mapper implementation takes event and returns a workload strategy.
        """
        ...
