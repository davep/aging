"""Provides a widget for showing a guide's menu."""

##############################################################################
# NGDB imports.
from ngdb import Entry, Menu, NortonGuide
from ngdb.link import Link

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
from ..messages import OpenEntry


##############################################################################
class TopLevelMenu(Option):
    """Class that holds a top-level menu option."""

    def __init__(self, menu_id: int, menu: Menu) -> None:
        """Initialise the object.

        Args:
            menu_id: The ID of the menu.
            menu: The menu to display.
        """
        self._menu = menu
        """The menu we're displaying."""
        super().__init__(f"[bold]{menu.title}[/]", id=str(menu_id))

    @property
    def first_child_id(self) -> str:
        """The ID of the first child option."""
        return str(self._menu[0].offset)


##############################################################################
class MenuPrompt(Option):
    """Class that holds a prompt for a menu."""

    def __init__(self, menu_id: int, prompt_id: int, menu_prompt: Link) -> None:
        """Initialise the object.

        Args:
            menu_id: The ID of the menu.
            prompt_id: The ID of the prompt.
            menu_prompt: The prompt to display.
        """
        self._menu_prompt = menu_prompt
        """The prompt that this object is displaying."""
        super().__init__(f"  {menu_prompt.text}", id=f"{menu_id}-{prompt_id}")

    @property
    def offset(self) -> int:
        """The offset of the entry related to this prompt."""
        return self._menu_prompt.offset


##############################################################################
class GuideMenu(EnhancedOptionList):
    """A widget for showing a Norton Guide's menu."""

    DEFAULT_CSS = """
    GuideMenu {
        width: auto;
        background: transparent;
        height: 1fr;
        border: none;

        &:focus {
            border: none;
        }

        &.--no-guide {
            display: none;
        }
    }
    """

    guide: var[NortonGuide | None] = var(None)
    """The guide whose menu we're showing."""

    current_entry: var[Entry | None] = var(None, init=False)
    """The currently-displayed entry."""

    def _highlight_menu_for_current_entry(self) -> None:
        """Ensure the menu for the current entry is highlighted.."""
        if (
            self.current_entry is None
            or not self.current_entry.parent.has_menu
            or not self.current_entry.parent.has_prompt
        ):
            self.highlighted = 0
            return
        try:
            self.highlighted = self.get_option_index(
                f"{self.current_entry.parent.menu}-{self.current_entry.parent.prompt}"
            )
        except OptionDoesNotExist:
            self.highlighted = 0

    def _watch_guide(self) -> None:
        """Handle the current guide being changed."""
        self.set_class(self.guide is None, "--no-guide")
        self.clear_options()
        if self.guide is not None:
            for menu_id, menu in enumerate(self.guide.menus):
                self.add_option(TopLevelMenu(menu_id, menu)).add_options(
                    (
                        MenuPrompt(menu_id, prompt_id, prompt)
                        if prompt.has_offset
                        else Option(prompt.text, disabled=True)
                    )
                    for prompt_id, prompt in enumerate(menu)
                )
            self._highlight_menu_for_current_entry()

    @on(EnhancedOptionList.OptionSelected)
    def _select_option(self, message: EnhancedOptionList.OptionSelected) -> None:
        """Handle an option being selected.

        Args:
            message: The message requesting the option is selected.
        """
        if isinstance(message.option, TopLevelMenu):
            self.highlighted = self.get_option_index(message.option.first_child_id)
        elif isinstance(message.option, MenuPrompt):
            self.post_message(OpenEntry(message.option.offset))


### guide_menu.py ends here
