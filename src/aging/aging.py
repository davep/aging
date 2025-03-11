"""The main application class."""

##############################################################################
# Python imports.
from argparse import Namespace

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
    HELP_ABOUT = """
    `AgiNG` is a terminal-based Norton Guide reader; it was created
    by and is maintained by [Dave Pearson](https://www.davep.org/); it is
    Free Software and can be [found on
    GitHub](https://github.com/davep/aging).
    """
    HELP_LICENSE = """
    AgiNG - A Norton Guide reader for the terminal.  \n    Copyright (C) 2025 Dave Pearson

    This program is free software: you can redistribute it and/or modify it
    under the terms of the GNU General Public License as published by the Free
    Software Foundation, either version 3 of the License, or (at your option)
    any later version.

    This program is distributed in the hope that it will be useful, but WITHOUT
    ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
    FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
    more details.

    You should have received a copy of the GNU General Public License along with
    this program. If not, see <https://www.gnu.org/licenses/>.
    """

    COMMANDS = set()

    def __init__(self, arguments: Namespace) -> None:
        """Initialise the application.

        Args:
            arguments: The command line arguments passed to the application.
        """
        self._arguments = arguments
        """The command line arguments passed to the application."""
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
        return Main(self._arguments)


### aging.py ends here
