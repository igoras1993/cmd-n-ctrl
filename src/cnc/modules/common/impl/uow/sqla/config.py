from dataclasses import dataclass


@dataclass(frozen=True, slots=True, unsafe_hash=True)
class SqlAlchemyUowConfig:
    uri: str
    echo: bool
