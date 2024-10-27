from datetime import datetime

from rich.text import Text
from textual.app import RenderResult, ComposeResult
from textual.events import Mount
from textual.reactive import Reactive
from textual.widget import Widget
from textual.widgets._header import HeaderIcon, HeaderTitle
from textual.dom import NoScreen


class HeaderClockSpace(Widget):
    """The space taken up by the clock on the right of the header."""

    DEFAULT_CSS = """
    HeaderClockSpace {
        dock: right;
        width: 20;
        padding: 0 1;
    }
    """

    def render(self) -> RenderResult:
        """Render the header clock space.

        Returns:
            The rendered space.
        """
        return ""


class HeaderDatedClock(HeaderClockSpace):
    """Display a clock on the right of the header."""

    DEFAULT_CSS = """
    HeaderDatedClock {
        background: $foreground-darken-1 5%;
        color: $text;
        text-opacity: 85%;
        content-align: center middle;
    }
    """

    time_format: Reactive[str] = Reactive("%X")

    def _on_mount(self, event: Mount) -> None:
        self.set_interval(1, callback=self.refresh, name="update header clock")

    def render(self) -> RenderResult:
        """Render the header clock.

        Returns:
            The rendered clock.
        """
        return Text(datetime.now().strftime(self.time_format))


class DatedHeader(Widget):
    """A header widget with icon and clock."""

    DEFAULT_CSS = """
    DatedHeader {
        dock: top;
        width: 100%;
        background: $foreground 5%;
        color: $text;
        height: 1;
    }
    """

    DEFAULT_CLASSES = ""

    icon: Reactive[str] = Reactive("⭘")
    """A character for the icon at the top left."""

    time_format: Reactive[str] = Reactive("%X")
    """Time format of the clock."""

    def __init__(
        self,
        show_clock: bool = False,
        *,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        icon: str | None = None,
        time_format: str | None = None,
    ):
        """Initialise the header widget.

        Args:
            show_clock: ``True`` if the clock should be shown on the right of the header.
            name: The name of the header widget.
            id: The ID of the header widget in the DOM.
            classes: The CSS classes of the header widget.
            icon: Single character to use as an icon, or `None` for default.
            time_format: Time format (used by strftime) for clock, or `None` for default.
        """
        super().__init__(name=name, id=id, classes=classes)
        self._show_clock = show_clock
        if icon is not None:
            self.icon = icon
        if time_format is not None:
            self.time_format = time_format

    def compose(self) -> ComposeResult:
        yield HeaderIcon().data_bind(DatedHeader.icon)
        yield HeaderTitle()
        yield (
            HeaderDatedClock().data_bind(DatedHeader.time_format)
            if self._show_clock
            else HeaderClockSpace()
        )

    @property
    def screen_title(self) -> str:
        """The title that this header will display.

        This depends on [`Screen.title`][textual.screen.Screen.title] and
        [`App.title`][textual.app.App.title].
        """
        screen_title = self.screen.title
        title = screen_title if screen_title is not None else self.app.title
        return title

    @property
    def screen_sub_title(self) -> str:
        """The sub-title that this header will display.

        This depends on [`Screen.sub_title`][textual.screen.Screen.sub_title] and
        [`App.sub_title`][textual.app.App.sub_title].
        """
        screen_sub_title = self.screen.sub_title
        sub_title = (
            screen_sub_title if screen_sub_title is not None else self.app.sub_title
        )
        return sub_title

    def _on_mount(self, event: Mount) -> None:
        async def set_title() -> None:
            try:
                self.query_one(HeaderTitle).text = self.screen_title
            except NoScreen:
                pass

        async def set_sub_title() -> None:
            try:
                self.query_one(HeaderTitle).sub_text = self.screen_sub_title
            except NoScreen:
                pass

        self.watch(self.app, "title", set_title)
        self.watch(self.app, "sub_title", set_sub_title)
        self.watch(self.screen, "title", set_title)
        self.watch(self.screen, "sub_title", set_sub_title)
