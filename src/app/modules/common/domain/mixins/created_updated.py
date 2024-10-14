from datetime import datetime
from dataclasses import dataclass
from uuid import UUID


@dataclass(eq=False, slots=True)
class CreatedUpdatedMixin:
    _created_at: datetime
    _created_by: UUID
    _updated_at: datetime | None
    _updated_by: UUID | None
