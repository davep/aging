"""Provides the widget that displays the entry's content."""

##############################################################################
# Python imports.
from typing import Iterable

##############################################################################
# NGDB imports.
from ngdb import Entry, Link, Long, Short
from ngdb.parser import RichText

##############################################################################
# Rich imports.
from rich.text import Text

##############################################################################
# Textual imports.
from textual import on
from textual.reactive import var
from textual.widgets.option_list import Option, OptionDoesNotExist

##############################################################################
# Textual enhanced imports.
from textual_enhanced.widgets import EnhancedOptionList

##############################################################################
# Local imports.
from ...messages import OpenEntry


##############################################################################
class TextualRichText(RichText):
    """A Rich parser that works better in Textual.

    I've run into an issue, and this might be a Textual <2.0 vs >=2.0 thing
    too, I don't know, where the output of the Rich parser works fine in the
    console, with Rich, but not great in Textual.

    This version tweaks how text is handled to make things work better.
    """

    def char(self, char: int) -> None:
        """Handle an individual character value.

        Args:
            char: The character value to handle.
        """
        self.text(chr(char).replace("\\", "\\\\"))


##############################################################################
class PlainLine(Option):
    """An option that just displays some text."""

    def __init__(self, line: str) -> None:
        """A plain line in an entry.

        Args:
            line: The line to display.
        """
        super().__init__(prompt := Text.from_markup(str(TextualRichText(line))))
        prompt.no_wrap = True


##############################################################################
class JumpLine(Option):
    """An option that jumps elsewhere in the guide."""

    def __init__(self, line: Link) -> None:
        """A line in an entry that links to another entry in a guide.

        Args:
            line: The line that links elsewhere.
        """
        self._line = line
        """The link to another location in the guide."""
        super().__init__(prompt := Text.from_markup(str(TextualRichText(line.text))))
        prompt.no_wrap = True

    @property
    def link(self) -> Link:
        """The link data for the jump line."""
        return self._line


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

    HELP = """
    ## Norton Guide entry content

    This is the content of the currently-selected entry in the Norton Guide.
    """

    entry: var[Entry | None] = var(None)
    """The [entry][ngdb.Entry] being viewed, or [`None`][None] if no entry."""

    def _watch_entry(self) -> None:
        """React to the entry being changed."""
        self.clear_options()
        if self.entry is not None:
            assert isinstance(self.entry, Iterable)
            if isinstance(self.entry, Short):
                self.add_options(
                    JumpLine(line) if line.has_offset else PlainLine(line.text)
                    for line in self.entry
                )
            elif isinstance(self.entry, Long):
                self.add_options(PlainLine(line) for line in self.entry)
            if self.option_count:
                self.highlighted = 0

    @on(EnhancedOptionList.OptionSelected)
    def _line_selected(self, message: EnhancedOptionList.OptionSelected) -> None:
        """Handle a line being selected in the entry.

        Args:
            message: The message telling us that a line was selected.
        """
        message.stop()
        if isinstance(message.option, PlainLine):
            return
        assert isinstance(message.option, JumpLine)
        if message.option.link.has_offset:
            self.post_message(OpenEntry(message.option.link.offset))

    def goto_line(self, line: int) -> None:
        """Move the highlight to the given line in the entry.

        Args:
            line: The line to jump to.
        """
        try:
            self.highlighted = line
        except OptionDoesNotExist:
            pass


### entry_content.py ends here
