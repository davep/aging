"""Provides the widget that displays the entry's content."""

##############################################################################
# NGDB imports.
from ngdb import Entry
from ngdb.parser import RichText

##############################################################################
# Rich imports.
from rich.text import Text

##############################################################################
# Textual imports.
from textual.reactive import var

##############################################################################
# Textual enhanced imports.
from textual_enhanced.widgets import EnhancedOptionList


##############################################################################
class EntryContent(EnhancedOptionList):
    """Widget that displays the content of a Norton Guide entry."""

    DEFAULT_CSS = """
    EntryContent {
        width: 1fr;
        height: 1fr;
        background: transparent;
        border: none;

        &:focus {
            border: none;
        }
    }
    """

    entry: var[Entry | None] = var(None)
    """The entry being viewed, or [`None`][None] if no entry."""

    def _watch_entry(self) -> None:
        """React to the entry being changed."""
        self.clear_options()
        if self.entry is not None:
            self.add_options(
                Text.from_markup(str(RichText(line))) for line in self.entry.lines
            )


### entry_content.py ends here
