"""Provides the widget for viewing a guide entry."""

##############################################################################
# NGDB imports.
from ngdb import Entry

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
    }
    """

    entry: var[Entry | None] = var(None)
    """The entry being viewed, or [`None`][None] if no entry."""

    def _watch_entry(self) -> None:
        """React to the entry being changed."""
        self.set_class(self.entry is None, "--no-entry")

    def compose(self) -> ComposeResult:
        """Compose the content of the widget."""
        yield EntryContent().data_bind(EntryViewer.entry)

    def goto_line(self, line: int) -> None:
        """Move the highlight to the given line in the entry.

        Args:
            line: The line to jump to.
        """
        self.query_one(EntryContent).goto_line(line)

    def focus(self, scroll_visible: bool = True) -> Self:
        self.query_one(EntryContent).focus(scroll_visible)
        return self


### widget.py ends here
