from dataclasses import dataclass
from typing import Mapping, Self

from cnc.modules.common.app.command.protocol import WorkloadMapper
from cnc.modules.common.app.uow.enum import WorkloadStrategy
from cnc.modules.common.domain.events.domain import DomainEvent


@dataclass
class DefaultWorkload(WorkloadMapper):
    """
    This is a [.WorkflowMapper][] that allows You to define detailed map
    of event classes to [.WorkloadStrategy][]. All events not covered
    by this map will be mapped to the `default` strategy.
    """

    default: WorkloadStrategy
    event_mapping: Mapping[type[DomainEvent], WorkloadStrategy]

    def get_event_workload(self, event: DomainEvent) -> WorkloadStrategy:
        """
        Mapper implementation takes event and returns a workload strategy.
        """
        try:
            workload = self.event_mapping[type(event)]
        except LookupError:
            workload = self.default

        return workload

    @classmethod
    def consistent(
        cls, event_mapping: Mapping[type[DomainEvent], WorkloadStrategy] | None = None
    ) -> Self:
        """
        Convenience constructor for creating [.DefaultWorkflow][] with consistent
        strategy as default.
        """
        return cls(event_mapping=event_mapping or {}, default=WorkloadStrategy.CONSISTENT)

    @classmethod
    def not_consistent(
        cls, event_mapping: Mapping[type[DomainEvent], WorkloadStrategy] | None = None
    ) -> Self:
        """
        Convenience constructor for creating [.DefaultWorkflow][] with not consistent
        strategy as default.
        """
        return cls(
            event_mapping=event_mapping or {}, default=WorkloadStrategy.NON_CONSISTENT
        )
