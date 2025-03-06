"""Provides the main application commands for the command palette."""

##############################################################################
# Textual enhanced imports.
from textual_enhanced.commands import (
    ChangeTheme,
    CommandHits,
    CommandsProvider,
    Help,
    Quit,
)

##############################################################################
# Local imports.
from ..commands import AddGuidesToDirectory, ChangeGuidesSide, ToggleGuides


##############################################################################
class MainCommands(CommandsProvider):
    """Provides some top-level commands for the application."""

    def commands(self) -> CommandHits:
        """Provide the main application commands for the command palette.

        Yields:
            The commands for the command palette.
        """
        yield AddGuidesToDirectory()
        yield ChangeGuidesSide()
        yield ChangeTheme()
        yield Help()
        yield ToggleGuides()
        yield Quit()


### main.py ends here
