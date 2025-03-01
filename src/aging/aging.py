"""The main application class."""

##############################################################################
# Textual enhanced imports.
from textual_enhanced.app import EnhancedApp

##############################################################################
# Local imports.
from . import __version__
from .screens import Main


##############################################################################
class Aging(EnhancedApp[None]):
    """The main application class."""

    HELP_TITLE = f"Aging {__version__}"
    HELP_ABOUT = "There will be more here."
    HELP_LICENSE = "License information will go here."

    def get_default_screen(self) -> Main:
        """Get the main screen for the application."""
        return Main()


### aging.py ends here
