"""Provides the guide directory widget."""

##############################################################################
# Python imports.
from dataclasses import replace
from typing import cast

##############################################################################
# NGDB imports.
from ngdb import NortonGuide

##############################################################################
# Textual imports.
from textual import on, work
from textual.binding import Binding
from textual.reactive import var
from textual.widgets.option_list import Option, OptionDoesNotExist

##############################################################################
# Textual enhanced imports.
from textual_enhanced.dialogs import ModalInput
from textual_enhanced.widgets import EnhancedOptionList

##############################################################################
# Local imports.
from ..data import Guide, Guides, save_guides
from ..messages import GuidesUpdated, OpenGuide


##############################################################################
class GuideView(Option):
    """A view of an option in the guide directory widget."""

    def __init__(self, guide: Guide) -> None:
        """Initialise the guide option."""
        self._guide = guide
        """The guide being handled by this option."""
        super().__init__(guide.title, id=str(guide.location))

    @property
    def guide(self) -> Guide:
        """The guide being handled by this option."""
        return self._guide


##############################################################################
class GuideDirectory(EnhancedOptionList):
    """A widget that holds and manages the Norton Guide directory."""

    DEFAULT_CSS = """
    GuideDirectory {
        width: auto;
        dock: left;
        background: transparent;
        height: 1fr;
        border: none;

        &:focus {
            border: none;
        }

        &.--dock-right {
            dock: right;
        }
    }
    """

    HELP = """
    ## Guide directory

    This is the directory of all the Norton Guide files that have been added
    to the application.
    """

    BINDINGS = [Binding("r", "rename", "Rename")]

    dock_right: var[bool] = var(False)
    """Should the directory dock to the right?"""

    guides: var[Guides] = var(Guides)
    """The guides in the directory."""

    guide: var[NortonGuide | None] = var(None)
    """The currently-selected guide.

    Note:
        This isn't the currently-highlighted guide, this is the guide that
        has been selected for display. Setting this will move the highlight
        in the widget to the correct position.
    """

    def _watch_guides(self) -> None:
        """React to the guides being changed."""
        with self.preserved_highlight:
            self.clear_options().add_options(
                GuideView(guide) for guide in sorted(self.guides)
            )
        self.refresh_bindings()

    def _watch_dock_right(self) -> None:
        """React to the dock toggle being changed."""
        self.set_class(self.dock_right, "--dock-right")

    def _watch_guide(self) -> None:
        """React to the current guide being set."""
        try:
            self.highlighted = (
                self.get_option_index(str(self.guide))
                if self.guide is not None
                else None
            )
        except OptionDoesNotExist:
            pass
        self.refresh_bindings()

    @on(EnhancedOptionList.OptionSelected)
    def _open_guide(self, message: EnhancedOptionList.OptionSelected) -> None:
        """React to a user's request to open a guide.

        Args:
            message: The message with the details of the request.
        """
        message.stop()
        assert isinstance(message.option, GuideView)
        self.post_message(OpenGuide(message.option.guide.location))

    def check_action(self, action: str, parameters: tuple[object, ...]) -> bool | None:
        """Check if an action is possible to perform right now.

        Args:
            action: The action to perform.
            parameters: The parameters of the action.

        Returns:
            `True` if it can perform, `False` or `None` if not.
        """
        if self.is_mounted:
            if action == "rename":
                return bool(self.guides)
        return True

    @work
    async def action_rename(self) -> None:
        """Rename the current guide."""
        if self.highlighted is None:
            return
        old_guide = cast(GuideView, self.get_option_at_index(self.highlighted)).guide
        if new_title := await self.app.push_screen_wait(
            ModalInput(initial=old_guide.title)
        ):
            guides = list(self.guides)
            if (
                guide_index := next(
                    (
                        index
                        for index, guide in enumerate(guides)
                        if guide == old_guide.location
                    ),
                    None,
                )
            ) is not None:
                guides[guide_index] = replace(old_guide, title=new_title)
            try:
                save_guides(guides)
            except IOError as error:
                self.notify(str(error), title="Unable to save guides", severity="error")
                return
            self.post_message(GuidesUpdated())


### guide_directory.py ends here
