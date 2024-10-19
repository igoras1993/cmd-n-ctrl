from textual.app import App
from textual.app import ComposeResult
from textual.widgets import Welcome


class CncHostApp(App):
    def compose(self) -> ComposeResult:
        yield Welcome()

    async def on_button_pressed(self) -> None:
        self.exit()
