from typing import Any, Callable
from sqlalchemy.orm.descriptor_props import DescriptorProperty

from app.modules.common.impl.tools.sqla.mapper_props.impl import (
    BaseModelInstancePropertyImpl,
)


class SimpleProperty[Instance, Value, SetterValue](DescriptorProperty):

    def __init__(
        self,
        getter: Callable[[Instance], Value],
        setter: Callable[[Instance, SetterValue], None] | None = None,
        deleter: Callable[[Instance], None] | None = None,
    ) -> None:
        super().__init__(attribute_options=None, _assume_readonly_dc_attributes=True)
        self.descriptor = property(getter, setter, deleter)


class PydanticProperty[Instance, Value](SimpleProperty[Instance, Value, Value]):

    def __init__(
        self,
        property_type: type[Value] | Any,
        serial_attr_name: str,
        cache_attr_name: str | None = None,
    ):
        self._serial_attr_name: str = serial_attr_name
        self._cache_attr_name: str | None = cache_attr_name
        self._impl = BaseModelInstancePropertyImpl(
            property_type, self._serial_attr_name, self._cache_attr_name
        )
        super().__init__(
            getter=self._impl.getter, setter=self._impl.setter, deleter=self._impl.deleter
        )
