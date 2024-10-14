from typing import Any

from pydantic import TypeAdapter
from app.modules.common.impl.tools.sqla.mapper_props.protocol import (
    InstancePropertyImplProtocol,
)


class BaseModelInstancePropertyImpl[Instance, Value](
    InstancePropertyImplProtocol[Instance, Value]
):
    def __init__(
        self,
        property_type: type[Value] | Any,
        serial_attr_name: str,
        cache_attr_name: str | None,
    ):
        self._property_type = property_type
        self._serial_attr_name = serial_attr_name
        self._cache_attr_name = self._process_cache_attr_name(cache_attr_name)
        self.deleter = None
        self.setter = self._setter

    def _process_cache_attr_name(self, given_name: str | None) -> str:
        if given_name is not None:
            return given_name
        else:
            return f"{self.serial_attr_name}_cache"

    @property
    def serial_attr_name(self) -> str:
        return self._serial_attr_name

    @property
    def cache_attr_name(self) -> str:
        return self._cache_attr_name

    def getter(self, inst: Instance) -> Value:
        try:
            return getattr(inst, self.cache_attr_name)
        except AttributeError:
            value = TypeAdapter(self._property_type).validate_python(
                getattr(inst, self.serial_attr_name)
            )
            setattr(
                inst,
                self.cache_attr_name,
                value,
            )
            return value

    def _setter(self, inst: Instance, value: Value) -> None:
        setattr(inst, self.cache_attr_name, value)
        setattr(
            inst,
            self.serial_attr_name,
            TypeAdapter(self._property_type).dump_python(value, mode="json"),
        )
