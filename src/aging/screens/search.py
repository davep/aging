"""Provides the search screen."""

##############################################################################
# NGDB imports.
from dataclasses import dataclass

from ngdb import NortonGuide

##############################################################################
# Textual imports.
from textual import on, work
from textual.app import ComposeResult
from textual.containers import HorizontalGroup, VerticalGroup
from textual.message import Message
from textual.screen import ModalScreen
from textual.widgets import Button, Checkbox, Input, Label, ProgressBar
from textual.worker import get_current_worker

##############################################################################
# Local imports.
from ..data.guides import Guide, Guides


##############################################################################
class Search(ModalScreen[None]):
    """Provides the global search screen."""

    DEFAULT_CSS = """
    Search {
        align: center middle;

        &> VerticalGroup {
            width: 80%;
            height: 80%;
            background: $panel;
            border: solid $border;

            &> HorizontalGroup {
                Input {
                    width: 1fr;
                }
            }
        }

        ProgressBar Bar {
            width: 1fr;
        }

        .--when-running {
            display: none;
        }
        .--when-stopped {
            display: block;
        }
        &.--running {
            .--when-running {
                display: block;
            }
            .--when-stopped {
                display: none;
            }
        }
    }
    """

    BINDINGS = [("escape", "dismiss(None)")]

    def __init__(self, guides: Guides, guide: NortonGuide | None) -> None:
        """Initialise the search screen.

        Args:
            guides: All the guides known to the application.
            guide: The current guide.
        """
        self._guides = guides
        """All the guides known to the application."""
        self._guide = guide
        """The current guide, if here is one."""
        super().__init__()

    def compose(self) -> ComposeResult:
        """Compose the content of the screen."""
        with VerticalGroup() as dialog:
            dialog.border_title = "Global Search"
            with HorizontalGroup():
                yield Input(placeholder="Search...")
                yield Checkbox("Global", True, id="global")
                yield Checkbox("Ignore Case", True, id="ignore_case")
                yield Button("Go", variant="primary", id="go", classes="--when-stopped")
                yield Button(
                    "Stop", variant="error", id="stop", classes="--when-running"
                )
            yield Label(id="current_guide", classes="--when-running")
            yield ProgressBar(id="guides_progress", classes="--when-running")

    @dataclass
    class Started(Message):
        """Message sent when a search has started."""

        searching: int
        """The number of guides we'll be searching."""

    @dataclass
    class NewGuide(Message):
        """Message sent when a new guide is being searched."""

        position: int
        """The position of the guide in the list of guides to search."""
        guide: Guide
        """The information about the guide being searched."""

    @on(Started)
    def _search_started(self, starting: Started) -> None:
        self.set_class(True, "--running")
        self.query_one("#guides_progress", ProgressBar).total = starting.searching

    @on(NewGuide)
    def _update_current_guide(self, current: NewGuide) -> None:
        self.query_one("#current_guide", Label).update(
            f"Searching {current.guide.title}"
        )
        self.query_one("#guides_progress", ProgressBar).progress = current.position

    @on(Input.Submitted)
    @on(Button.Pressed, "#go")
    @work(thread=True, exclusive=True)
    def _start_search(self) -> None:
        """Start a new search."""
        guides = self._guides
        if not self.query_one("#global", Checkbox).value:
            if self._guide is None:
                self.notify(
                    "Unable to perform a non-global search when no guide is open",
                    title="Can't search",
                    severity="error",
                )
                return
            guides = [Guide(self._guide.title, self._guide.path)]
        worker = get_current_worker()
        self.post_message(self.Started(len(guides)))
        from time import sleep

        for position, guide in enumerate(sorted(guides)):
            if worker.is_cancelled:
                return
            self.post_message(self.NewGuide(position + 1, guide))
            sleep(0.05)


### search.py ends here
