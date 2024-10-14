from copy import copy
from typing import Generator, Sequence
from app.modules.common.domain.entity import Entity
from app.modules.common.domain.events.domain import DomainEvent


class AggregateRoot(Entity):

    @property
    def events(self) -> Sequence[DomainEvent]:
        return copy(self._event_store)

    def stage_event(self, event: DomainEvent):
        self._event_store.append(event)

    def consume_events(self) -> Generator[DomainEvent, None, None]:
        """
        Yields one event by another, each time removing
        it from the collection of aggregate event state.
        """
        store = self._event_store
        while store:
            event = store.pop(0)
            yield event

    @property
    def _event_store(self) -> list[DomainEvent]:
        try:
            events = getattr(self, "_events")
        except AttributeError:
            events = list()
            setattr(self, "_events", events)

        return events
