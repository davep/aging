"""Provides a dialog for showing information about a guide."""

##############################################################################
# Python imports.
from datetime import datetime

##############################################################################
# Humanize imports.
from humanize import naturalsize

##############################################################################
# NGDB imports.
from ngdb import NortonGuide, make_dos_like

##############################################################################
# Textual imports.
from textual import on
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Label

##############################################################################
# Textual enhanced imports.
from textual_enhanced.tools import add_key


##############################################################################
class Title(Label):
    """A widget to show a title."""

    DEFAULT_CSS = """
    Title {
        text-style: bold;
        color: $accent;
        width: 100%;
    }
    """


##############################################################################
class Data(Label):
    """A widget to show data."""


##############################################################################
class About(ModalScreen[None]):
    """A dialog for showing information about a Norton Guide."""

    DEFAULT_CSS = """
    About {
        align: center middle;
        &> Vertical {
            width: auto;
            height: auto;
            background: $panel;
            border: solid $border;
        }

        #buttons {
            align: center middle;
            border-top: solid $border;
            width: 100%;
            height: auto;
        }

        Title, {
            margin: 1 2 0 2;
        }
        Data {
            margin: 0 2 1 2;
        }

        #credits {
            margin: 1 2 1 2;
            border-title-align: right;
            border-title-color: $accent;
            border: solid $border;
            background: $secondary;
        }
    }
    """

    BINDINGS = [("escape", "dismiss(None)")]

    def __init__(self, guide: NortonGuide) -> None:
        """Initialise the object.

        Args:
            guide: The guide to show the details for.
        """
        self._guide = guide
        """The guide we're viewing."""
        super().__init__()

    def compose(self) -> ComposeResult:
        """Compose the content of the screen."""
        with Vertical() as dialog:
            dialog.border_title = f"About {self._guide.path.name}"
            if any(line.strip() for line in self._guide.credits):
                yield (
                    data := Data(
                        "\n".join(make_dos_like(line) for line in self._guide.credits),
                        id="credits",
                    )
                )
                data.border_title = "Credits"
            yield Title("Made With:")
            yield Data(self._guide.made_with)
            yield Title("File:")
            yield Data(str(self._guide.path))
            yield Title("Size:")
            yield Data(naturalsize(self._guide.path.stat().st_size))
            yield Title("Created:")
            yield Data(
                f"{datetime.fromtimestamp(int(self._guide.path.stat().st_ctime))}"
            )
            with Horizontal(id="buttons"):
                yield Button(add_key("Close", "Esc", self))

    @on(Button.Pressed)
    def _close_about(self) -> None:
        """Close the about dialog."""
        self.dismiss(None)


### about.py ends here
