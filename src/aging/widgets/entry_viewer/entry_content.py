"""Provides the widget that displays the entry's content."""

##############################################################################
# Python imports.
from typing import Final

##############################################################################
# NGDB imports.
from ngdb import Link, Long, MarkupText, Short, make_dos_like
from rich.markup import escape

##############################################################################
# Rich imports.
from rich.segment import Segment
from rich.text import Text

##############################################################################
# Textual imports.
from textual import on
from textual.reactive import var
from textual.strip import Strip
from textual.widgets.option_list import Option, OptionDoesNotExist

##############################################################################
# Textual enhanced imports.
from textual_enhanced.widgets import EnhancedOptionList

##############################################################################
# Typing extension imports.
from typing_extensions import Self

##############################################################################
# Local imports.
from ...messages import OpenEntry


##############################################################################
class TextualText(MarkupText):
    """Norton Guide source parser for Textual-based markup."""

    def char(self, char: int) -> None:
        """Handle an individual character value.

        Args:
            char: The character value to handle.
        """
        self.text(chr(char))

    def text(self, text: str) -> None:
        """Handle some text.

        Args:
            text: The text to handle.
        """
        super().text(escape(make_dos_like(text)))

    def open_markup(self, cls: str) -> str:
        """Open a section of markup.

        Args:
            cls: The class of markup to open.

        Returns:
            The opening markup.
        """
        return f"[{cls}]"

    def close_markup(self, cls: str) -> str:
        """Close a section of markup.

        Args:
            cls: The class of markup to close.

        Returns:
            The closing markup.
        """
        return "[/]"

    COLOUR_MAP: Final[dict[int, str]] = {
        0: "000000",
        1: "0000AA",
        2: "00AA00",
        3: "00AAAA",
        4: "AA0000",
        5: "AA00AA",
        6: "AA5500",
        7: "AAAAAA",
        8: "555555",
        9: "5555FF",
        10: "55FF55",
        11: "55FFFF",
        12: "FF5555",
        13: "FF55FF",
        14: "FFFF55",
        15: "FFFFFF",
    }
    """DOS colour map."""

    def colour(self, colour: int) -> None:
        """Handle a request for a colour attribute.

        Args:
            colour: The colour attribute to handle.
        """
        self.begin_markup(
            f"#{self.COLOUR_MAP[colour & 0xF]} on #{self.COLOUR_MAP[colour >> 4 & 0xF]}"
        )

    def bold(self) -> None:
        """Start a bold section of text."""
        self.begin_markup("bold")

    def unbold(self) -> None:
        """End a bold section of text."""
        self.end_markup()

    def reverse(self) -> None:
        """Start a reversed section of text."""
        self.begin_markup("reverse")

    def unreverse(self) -> None:
        """End a reversed section of text."""
        self.end_markup()

    def underline(self) -> None:
        """Start an underlined section of text."""
        self.begin_markup("underline")

    def ununderline(self) -> None:
        "End an underlined section of text."
        self.end_markup()

    @property
    def as_rich_text(self) -> Text:
        """The text marked up as a [Rich text object][rich.Text]."""
        return Text.from_markup(str(self))


##############################################################################
class PlainLine(Option):
    """An option that just displays some text."""

    def __init__(self, line: str) -> None:
        """A plain line in an entry.

        Args:
            line: The line to display.
        """
        super().__init__(prompt := TextualText(line).as_rich_text)
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
        super().__init__(prompt := TextualText(line.text).as_rich_text)
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

    entry: var[Short | Long | None] = var(None)
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
            if self.option_count:
                # NOTE: This should simply be:
                #
                # self.goto_line(0)
                #
                # However https://github.com/Textualize/textual/issues/5632
                # means the scrollbar goes FUBAR, hence the rather bonkers
                # "go to the end, then go back to the start".
                #
                # This workaround will be removed when textual#5632 is no
                # longer a problem.
                self.goto_line(len(self.entry.lines) - 1).goto_line(0)

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

    def goto_line(self, line: int) -> Self:
        """Move the highlight to the given line in the entry.

        Args:
            line: The line to jump to.

        Returns:
            Self.
        """
        try:
            self.highlighted = line
        except OptionDoesNotExist:
            pass
        return self

    def render_line(self, y: int) -> Strip:
        """Render a line in the display.

        Args:
            y: The line to render.

        Returns:
            The strip that renders the requested line.

        This method simply overrides the version in
        [`OptionList`][textual.widgets.OptionList] in the case where we're
        rendering the highlighted line. Textual's approach when there are
        colours in the prompt is to let those win over the highlighted
        component class; for this widget I want the highlight to be plain
        text, no overriding colours.
        """
        strip = super().render_line(y)
        if self.scroll_offset.y + y == self.highlighted:
            if highlight := self.get_visual_style("option-list--option-highlighted"):
                strip = Strip(
                    [
                        Segment(
                            text,
                            style.without_color + highlight.rich_style
                            if style is not None
                            else None,
                            control,
                        )
                        for text, style, control in strip
                    ]
                )

        return strip


### entry_content.py ends here
