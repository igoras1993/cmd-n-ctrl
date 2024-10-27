from textual.app import App
from textual.app import ComposeResult
from textual.widgets import Welcome, TabbedContent, TabPane
from cnc.modules.controller.ui.textual.dashboard import Dashboard
from cnc.modules.gateway.ui.textual.host.ids import DomId
from cnc.modules.gateway.ui.textual.host.widgets.header import DatedHeader


class CncHostApp(App):
    TITLE: str | None = "Command and control"

    def compose(self) -> ComposeResult:
        yield DatedHeader(
            show_clock=True,
            icon="🐗",
            id=DomId.host_header.value,
            time_format=r"%a %d.%m, %H:%M",
        )
        with TabbedContent(id=DomId.host_tabs):
            with TabPane("Dashboard"):
                yield Dashboard()
            with TabPane("Next tab"):
                yield Welcome()

    async def on_button_pressed(self) -> None:
        self.exit()
