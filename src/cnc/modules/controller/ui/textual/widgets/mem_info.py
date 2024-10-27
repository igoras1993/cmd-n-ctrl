from typing import Protocol
import psutil

from cnc.modules.common.ui.textual.tools.css import CssLoader
from cnc.modules.common.ui.textual.widgets.device_info import DeviceInfo


class VirtualMemoryData(Protocol):
    @property
    def percent(self) -> float: ...

    @property
    def total(self) -> float: ...

    @property
    def available(self) -> float: ...


class MemInfo(DeviceInfo):

    css_loader = CssLoader()

    @property
    def latest_label(self) -> str:
        return "LATEST [GiB]"

    @property
    def total_label(self) -> str:
        return "TOTAL [GiB]"

    async def update_metrics(self) -> None:
        virtual_mem = await self.get_virtual_memory()
        used_gb = (virtual_mem.total - virtual_mem.available) / 1073741824
        self.metrics.append(used_gb)
        self.mutate_reactive(self.__class__.metrics)
        self.total = virtual_mem.total / 1073741824

    async def get_virtual_memory(self) -> VirtualMemoryData:
        return psutil.virtual_memory()

    async def get_metric_value(self) -> float:
        return (await self.get_virtual_memory()).percent
