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
from ..commands import (
    AddGuidesToDirectory,
    ChangeGuidesSide,
    CopyEntrySourceToClipboard,
    CopyEntryToClipboard,
    GoToNextEntry,
    GoToPreviousEntry,
    ToggleGuides,
)


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
        yield from self.maybe(CopyEntryToClipboard)
        yield from self.maybe(CopyEntrySourceToClipboard)
        yield from self.maybe(GoToNextEntry)
        yield from self.maybe(GoToPreviousEntry)
        yield Help()
        yield Quit()
        yield ToggleGuides()


### main.py ends here
