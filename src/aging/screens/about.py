"""Provides a dialog for showing information about a guide."""

##############################################################################
# NGDB imports.
from ngdb import NortonGuide, make_dos_like

##############################################################################
# Textual imports.
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.screen import ModalScreen
from textual.widgets import Label


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
    }
    """

    BINDINGS = [("escape, f3", "dismiss(None)")]

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
            yield Label("\n".join(make_dos_like(line) for line in self._guide.credits))


### about.py ends here
