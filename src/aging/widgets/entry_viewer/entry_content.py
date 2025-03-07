"""Provides the widget that displays the entry's content."""

##############################################################################
# NGDB imports.
from ngdb import Entry, Long, Short
from ngdb.link import Link
from ngdb.parser import RichText

##############################################################################
# Rich imports.
from rich.text import Text

##############################################################################
# Textual imports.
from textual.reactive import var
from textual.widgets.option_list import Option

##############################################################################
# Textual enhanced imports.
from textual_enhanced.widgets import EnhancedOptionList


##############################################################################
class PlainLine(Option):
    """An option that just displays some text."""

    def __init__(self, line: str) -> None:
        """The link to another location in the guide."""
        super().__init__(Text.from_markup(str(RichText(line))))


##############################################################################
class JumpLine(Option):
    """An option that jumps elsewhere in the guide."""

    def __init__(self, line: Link) -> None:
        self._line = line
        """The link to another location in the guide."""
        super().__init__(Text.from_markup(str(RichText(line.text))))


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
    """The [entry][ngdb.Entry] being viewed, or [`None`][None] if no entry."""

    def _watch_entry(self) -> None:
        """React to the entry being changed."""
        self.clear_options()
        if self.entry is not None:
            if isinstance(self.entry, Short):
                self.add_options(
                    JumpLine(line) if line.has_offset else PlainLine(line.text)
                    for line in self.entry
                )
            elif isinstance(self.entry, Long):
                self.add_options(PlainLine(line) for line in self.entry)


### entry_content.py ends here
