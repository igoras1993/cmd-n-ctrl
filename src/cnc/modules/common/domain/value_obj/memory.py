from dataclasses import dataclass
from enum import IntEnum
from typing import Self


class MemUnit(IntEnum):
    B = 1
    KiB = 2**10
    MiB = 2**20
    GiB = 2**30


@dataclass(frozen=True)
class Memory:
    amount: float
    unit: MemUnit = MemUnit.B

    def value_as(self, unit: MemUnit) -> float:
        """
        Convert to the floating point value in given units
        """
        return self.amount * (self.unit / unit)

    @property
    def bytes(self) -> float:
        return self.value_as(MemUnit.B)

    def __eq__(self, value: object) -> bool:
        if isinstance(value, Memory):
            return self.bytes == value.bytes
        else:
            return False

    def __add__(self, other: object) -> "Memory":
        if isinstance(other, Memory):
            return Memory(self.bytes + other.bytes, unit=MemUnit.B)
        else:
            return NotImplemented

    def __sub__(self, other: object) -> "Memory":
        if isinstance(other, Memory):
            return Memory(self.bytes - other.bytes, unit=MemUnit.B)
        else:
            return NotImplemented

    def __mul__(self, other: object) -> "Memory":
        if isinstance(other, float | int):
            return Memory(self.bytes * other, unit=MemUnit.B)
        else:
            return NotImplemented


@dataclass(frozen=True)
class MemoryUsage:
    """
    Memory usage summary
    """

    available: Memory
    total: Memory

    @classmethod
    def from_used(
        cls,
        used: float,
        total: float,
        used_unit: MemUnit = MemUnit.B,
        total_unit: MemUnit = MemUnit.B,
    ) -> Self:
        """
        Create memory usage from `used` and `total` pair.

        Args:
            used: Amount of used memory
            total: Total memory
        """
        return cls(
            available=Memory(total - used, used_unit), total=Memory(total, total_unit)
        )

    @classmethod
    def from_available(
        cls,
        available: float,
        total: float,
        available_unit: MemUnit = MemUnit.B,
        total_unit: MemUnit = MemUnit.B,
    ) -> Self:
        """
        Create memory usage from `used` and `total` pair.

        Args:
            available: Amount of available memory
            total: Total memory
        """
        return cls(
            available=Memory(available, available_unit), total=Memory(total, total_unit)
        )

    @property
    def used(self) -> Memory:
        return self.total - self.available
