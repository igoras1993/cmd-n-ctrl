import psutil

from cnc.modules.common.ui.textual.tools.css import CssLoader
from cnc.modules.common.ui.textual.widgets.device_info import DeviceInfo


class CpuInfo(DeviceInfo):

    css_loader = CssLoader()

    @property
    def latest_label(self) -> str:
        return "LATEST [%]"

    @property
    def total_label(self) -> str:
        return "TOTAL [%]"

    async def get_metric_value(self) -> float | None:
        return psutil.cpu_percent()
