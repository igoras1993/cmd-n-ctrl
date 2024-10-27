from collections import deque
from textual.app import ComposeResult
from textual.reactive import reactive
from textual.widgets import Sparkline, Static, DataTable

from cnc.modules.common.ui.textual.tools.css import CssLoader


class DeviceInfo(Static):

    css_loader = CssLoader()

    interval: reactive[int] = reactive(1)
    metrics: reactive[deque[float]] = reactive(lambda: deque([0] * 20, maxlen=20))
    total: reactive[float | None] = reactive(100)

    @property
    def latest_label(self) -> str:
        return "LATEST"

    @property
    def total_label(self) -> str:
        return "TOTAL"

    def compose(self) -> ComposeResult:
        yield Sparkline().data_bind(data=self.__class__.metrics)
        yield DataTable(
            show_header=False,
            show_row_labels=True,
            fixed_rows=2,
            fixed_columns=1,
        )

    async def on_mount(self) -> None:
        self.set_interval(self.interval, self.update_metrics)
        self.watch(self, "total", self.on_total_change, init=False)
        self.watch(self, "metrics", self.on_metrics_change, init=False)
        await self.init_data_table(self.query_one(DataTable))

    async def init_data_table(self, dt: DataTable) -> None:
        dt.add_column(label="", key="values_column")
        dt.add_row(
            await self.get_dt_latest_value(), label=self.latest_label, key="latest_row"
        )
        dt.add_row(
            await self.get_dt_total_value(), label=self.total_label, key="total_row"
        )

    async def update_dt_latest_value(self, dt: DataTable) -> None:
        dt.update_cell(
            row_key="latest_row",
            column_key="values_column",
            value=await self.get_dt_latest_value(),
        )

    async def update_dt_total_value(self, dt: DataTable) -> None:
        dt.update_cell(
            row_key="total_row",
            column_key="values_column",
            value=await self.get_dt_total_value(),
        )

    async def update_metrics(self) -> None:
        value = await self.get_metric_value()
        if value is not None:
            self.metrics.append(value)
            self.mutate_reactive(self.__class__.metrics)

    async def get_dt_latest_value(self) -> str:
        try:
            return f"{self.metrics[-1]:.2f}"
        except IndexError:
            return "---"

    async def get_dt_total_value(self) -> str:
        if self.total is None:
            return "---"
        else:
            return f"{self.total:.2f}"

    async def on_total_change(self) -> None:
        dt = self.query_one(DataTable)
        await self.update_dt_total_value(dt)

    async def on_metrics_change(self) -> None:
        dt = self.query_one(DataTable)
        await self.update_dt_latest_value(dt)

    async def get_metric_value(self) -> float | None:
        """
        Get new metric value. New value will be pushed into `metrics` deque.
        If this method returns `None`, `metrics` will not be updated.
        """
        return None


print(DeviceInfo.DEFAULT_CSS)
