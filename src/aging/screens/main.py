"""Provides the main screen."""

##############################################################################
# Textual imports.
from textual.app import ComposeResult
from textual.widgets import Footer, Header

##############################################################################
# Textual enhanced imports.
from textual_enhanced.commands import ChangeTheme, Command, Help, Quit
from textual_enhanced.screen import EnhancedScreen

##############################################################################
# Local imports.
from .. import __version__
from ..providers import MainCommands


##############################################################################
class Main(EnhancedScreen[None]):
    """The main screen for the application."""

    TITLE = f"Aging v{__version__}"

    HELP = """
    ## Main application keys and commands

    The following key bindings and commands are available:
    """

    COMMAND_MESSAGES = (
        # Keep these together as they're bound to function keys and destined
        # for the footer.
        Help,
        ChangeTheme,
        Quit,
    )

    BINDINGS = Command.bindings(*COMMAND_MESSAGES)
    COMMANDS = {MainCommands}

    def compose(self) -> ComposeResult:
        """Compose the content of the main screen."""
        yield Header()
        yield Footer()


### main.py ends here
