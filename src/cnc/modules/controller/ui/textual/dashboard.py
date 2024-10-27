from textual.widgets import Static, Collapsible
from textual.app import ComposeResult

from cnc.modules.controller.ui.textual.widgets.cpu_info import CpuInfo
from cnc.modules.controller.ui.textual.widgets.mem_info import MemInfo


class Dashboard(Static):
    def compose(self) -> ComposeResult:
        with Collapsible(title="CPU Usage", collapsed=False):
            yield CpuInfo()
        with Collapsible(title="Memory Usage", collapsed=False):
            yield MemInfo()
