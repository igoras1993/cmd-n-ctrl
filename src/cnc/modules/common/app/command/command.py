from abc import ABC, abstractmethod
from typing import Sequence

from plug_in import Hosted

from cnc.shared.ioc.root import root_router

from cnc.modules.common.app.uow.uow import UnitOfWork
from cnc.modules.common.app.command.protocol import WorkloadMapper
from cnc.modules.common.domain.agg_root import AggregateRoot


class Command(ABC):
    """
    Helper class for creating a command. Inherit after this ABC and implement
    [.Command.process_command][] to be automatically coordinated with [.UnitOfWork].

    You do not have to inherit, but then You must manage UoW stuff by yourself.
    """

    @abstractmethod
    async def process_command(self) -> tuple[Sequence[AggregateRoot], WorkloadMapper]:
        """
        Implementation of this method should do everything that command logic
        does, and then return a sequence of [.AggregateRoot][] objects engaged
        in command execution; along with [.WorkloadMapper][] that will provide
        [.WorkloadStrategy][] for handling domain events.
        """
        ...

    @root_router.manage()
    async def execute(self, uow: UnitOfWork = Hosted()) -> None:

        async with uow.start():
            agg_roots, workload_mapper = await self.process_command()

            # Flush before consuming events
            await uow.get_repository().flush(None)

            for event in (
                event for agg_root in agg_roots for event in agg_root.consume_events()
            ):
                await uow.push(
                    msg=event, workload_strategy=workload_mapper.get_event_workload(event)
                )
