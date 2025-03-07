"""Provides the widget for viewing a guide entry."""

##############################################################################
# NGDB imports.
from ngdb import Entry

##############################################################################
# Textual imports.
from textual.containers import VerticalGroup
from textual.reactive import var


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


### widget.py ends here
