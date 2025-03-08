"""Provides a modal screen for selecting a see-also item."""

##############################################################################
# NGDB imports.
from ngdb import Long
from ngdb.link import Link

##############################################################################
# Textual imports.
from textual import on
from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.widgets.option_list import Option

##############################################################################
# Textual enhanced imports.
from textual_enhanced.widgets import EnhancedOptionList


##############################################################################
class SeeAlsoItem(Option):
    """An item to also see."""

    def __init__(self, see_also: Link) -> None:
        """Initialise the object.

        Args:
            see_also: The item to see also.
        """
        self._see_also = see_also
        """The item to see also."""
        super().__init__(see_also.text, id=str(see_also.offset))

    @property
    def offset(self) -> int:
        """The offset of the entry for the see-also item."""
        return self._see_also.offset


##############################################################################
class SeeAlsoMenu(ModalScreen[int | None]):
    """A menu for picking a see-also for an entry."""

    DEFAULT_CSS = """
    SeeAlsoMenu {
        align: center middle;
        EnhancedOptionList {
            width: auto;
            min-width: 30;
            height: auto;
            padding: 1 2;
            background: $panel-lighten-1;
            &, &:focus {
                border: blank $border;
            }
        }
    }
    """

    BINDINGS = [("escape", "dismiss(None)")]

    def __init__(self, entry: Long) -> None:
        """Initialise the object.

        Args:
            entry: The long entry to show the see-alsos for.
        """
        super().__init__()
        self._entry = entry
        """The entry to show the see-also items for."""

    def compose(self) -> ComposeResult:
        """Compose the content of the screen."""
        yield (
            see_alsos := EnhancedOptionList(
                *[SeeAlsoItem(see_also) for see_also in self._entry.see_also]
            )
        )
        see_alsos.border_title = "See also..."

    @on(EnhancedOptionList.OptionSelected)
    def _jump_to_entry(self, message: EnhancedOptionList.OptionSelected) -> None:
        """Jump to a chosen see-also item.

        Args:
            message: The message requesting the see-also item be selected.
        """
        assert isinstance(message.option, SeeAlsoItem)
        self.dismiss(message.option.offset)


### see_also.py ends here
