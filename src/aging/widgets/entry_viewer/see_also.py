"""Provides a widget for seeing and navigating see-also items."""

##############################################################################
# NGDB imports.
from ngdb import Link, Long, Short

##############################################################################
# Textual imports.
from textual import on
from textual.app import ComposeResult
from textual.containers import HorizontalScroll
from textual.events import Click
from textual.reactive import var
from textual.widgets import Label

##############################################################################
# Typing extension imports.
from typing_extensions import Self

##############################################################################
# Local imports.
from ...messages import OpenEntry


##############################################################################
class SeeAlsoOption(Label, can_focus=True):
    """A widget that lets the user pick a see-also item."""

    DEFAULT_CSS = """
    SeeAlsoOption {
        padding: 0 1;
        margin: 0 1;

        &:focus {
            color: $block-cursor-foreground;
            background: $block-cursor-background;
            text-style: $block-cursor-text-style;
        }

        &:hover:blur {
            background: $block-hover-background;
        }
    }
    """

    BINDINGS = [("enter, space", "jump")]

    HELP = """
    ## See also option

    This is a related entry to the entry you are currently viewing. Either
    press <kbd>Enter</kbd> or click on the option with the mouse to jump to
    it.
    """

    def __init__(self, see_also: Link) -> None:
        """Initialise the object.

        Args:
            see_also: The see-also item to link to.
        """
        self._see_also = see_also
        """The see-also item to display and link to."""
        super().__init__(see_also.text)

    @on(Click)
    def action_jump(self) -> None:
        """Jump to the entry for this see-also item."""
        self.post_message(OpenEntry(self._see_also.offset))


##############################################################################
class SeeAlsos(HorizontalScroll, can_focus=False):
    """The container for see-also links."""

    DEFAULT_CSS = """
    SeeAlsos {
        height: auto;
        width: 1fr;
        display: none;
        scrollbar-size-horizontal: 0;

        &.--see-also {
            display: block;
        }
    }
    """

    BINDINGS = [("up, left", "previous"), ("down, right", "next")]

    HELP = """
    ## See also items

    This is the collection of related entries for the currently-selected
    Norton Guide entry.
    """

    entry: var[Short | Long | None] = var(None)
    """The entry being viewed, or [`None`][None] if no entry."""

    async def _watch_entry(self) -> None:
        """React to the entry being changed."""
        self.set_class(
            self.entry is not None
            and isinstance(self.entry, Long)
            and self.entry.has_see_also,
            "--see-also",
        )
        await self.query(SeeAlsoOption).remove()
        if isinstance(self.entry, Long) and (
            see_alsos := [SeeAlsoOption(see_also) for see_also in self.entry.see_also]
        ):
            await self.mount_all(see_alsos)
            see_alsos[0].add_class("--first")
            see_alsos[-1].add_class("--last")

    def compose(self) -> ComposeResult:
        """Compose the content of the widget."""
        yield Label("See also:")

    def focus(self, scroll_visible: bool = True) -> Self:
        self.query(SeeAlsoOption).first().focus(scroll_visible)
        return self

    def action_previous(self) -> None:
        """Jump to the previous see-also, with wrap-around."""
        if self.screen.focused is None:
            return
        if "--first" in self.screen.focused.classes:
            self.query_one(".--last").focus()
        else:
            self.screen.focus_previous()

    def action_next(self) -> None:
        """Jump to the next see-also, with wrap-around."""
        if self.screen.focused is None:
            return
        if "--last" in self.screen.focused.classes:
            self.query_one(".--first").focus()
        else:
            self.screen.focus_next()


### see_also.py ends here
