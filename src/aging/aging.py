"""The main application class."""

##############################################################################
# Textual imports.
from textual.app import InvalidThemeError

##############################################################################
# Textual enhanced imports.
from textual_enhanced.app import EnhancedApp

##############################################################################
# Local imports.
from . import __version__
from .data import (
    load_configuration,
    update_configuration,
)
from .screens import Main


##############################################################################
class AgiNG(EnhancedApp[None]):
    """The main application class."""

    HELP_TITLE = f"AgiNG {__version__}"
    HELP_ABOUT = "There will be more here."
    HELP_LICENSE = "License information will go here."

    COMMANDS = set()

    def __init__(self) -> None:
        """Initialise the application.

        Args:
            The command line arguments passed to the application.
        """
        super().__init__()
        configuration = load_configuration()
        if configuration.theme is not None:
            try:
                self.theme = configuration.theme
            except InvalidThemeError:
                pass

    def watch_theme(self) -> None:
        """Save the application's theme when it's changed."""
        with update_configuration() as config:
            config.theme = self.theme

    def get_default_screen(self) -> Main:
        """Get the main screen for the application."""
        return Main()


### aging.py ends here
