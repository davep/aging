"""Provides the widget that displays the entry's content."""

##############################################################################
# Python imports.
from functools import singledispatchmethod
from typing import Iterator

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
    """The entry being viewed, or [`None`][None] if no entry."""

    @singledispatchmethod
    def _content(self, entry: Entry) -> Iterator[Option]:
        """Generate the content for the given entry.

        Args:
            entry: The entry to generate the content for.

        Yields:
            Lines for the content.
        """
        yield from ()

    @_content.register
    def _(self, entry: Short) -> Iterator[Option]:
        return ((JumpLine if line.has_offset else PlainLine)(line) for line in entry)

    @_content.register
    def _(self, entry: Long) -> Iterator[Option]:
        return (PlainLine(line) for line in entry)

    def _watch_entry(self) -> None:
        """React to the entry being changed."""
        self.clear_options()
        if self.entry is not None:
            self.add_options(self._content(self.entry))


### entry_content.py ends here
