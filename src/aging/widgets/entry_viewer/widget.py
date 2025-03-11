"""Provides the widget for viewing a guide entry."""

##############################################################################
# NGDB imports.
from ngdb import Long, Short

##############################################################################
# Textual imports.
from textual.app import ComposeResult
from textual.containers import VerticalGroup
from textual.reactive import var

##############################################################################
# Typing extension imports.
from typing_extensions import Self

##############################################################################
# Local imports.
from .entry_content import EntryContent
from .see_also import SeeAlsos


##############################################################################
class EntryViewer(VerticalGroup):
    """The entry viewer widget."""

    DEFAULT_CSS = """
    EntryViewer {
        height: 1fr;
        display: block;

        &.--no-entry {
            display: none;
        }

        SeeAlsos {
            border-top: solid $panel;
        }

        &:focus-within SeeAlsos {
            border-top: solid $border;
        }
    }
    """

    HELP = """
    ## Guide entry panel

    This panel contains the content of the currently-selected Norton Guide
    entry.
    """

    classic_view: var[bool] = var(False)
    """Should we view the guide in the classic colour scheme?"""

    entry: var[Short | Long | None] = var(None)
    """The entry being viewed, or [`None`][None] if no entry."""

    def _watch_entry(self) -> None:
        """React to the entry being changed."""
        self.set_class(self.entry is None, "--no-entry")

    def compose(self) -> ComposeResult:
        """Compose the content of the widget."""
        yield EntryContent().data_bind(EntryViewer.classic_view, EntryViewer.entry)
        yield SeeAlsos().data_bind(EntryViewer.entry)

    def goto_line(self, line: int) -> None:
        """Move the highlight to the given line in the entry.

        Args:
            line: The line to jump to.
        """
        self.query_one(EntryContent).goto_line(line)

    def see_also(self) -> None:
        """Place focus in the see-also area of the widget."""
        self.query_one(SeeAlsos).focus()

    @property
    def seeing_also(self) -> bool:
        """Is focus within the see-also area of the viewer?"""
        return bool(self.query("SeeAlsos:focus-within"))

    def focus(self, scroll_visible: bool = True) -> Self:
        self.query_one(EntryContent).focus(scroll_visible)
        return self


### widget.py ends here
