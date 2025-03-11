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
    AboutTheGuide,
    AddGuidesToDirectory,
    BrowseForGuide,
    ChangeGuidesSide,
    CopyEntrySourceToClipboard,
    CopyEntryTextToClipboard,
    Escape,
    GoToNextEntry,
    GoToParent,
    GoToPreviousEntry,
    JumpToMenu,
    SaveEntrySource,
    SaveEntryText,
    SearchForGuide,
    SeeAlso,
    ToggleClassicView,
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
        yield from self.maybe(AboutTheGuide)
        yield AddGuidesToDirectory()
        yield BrowseForGuide()
        yield ChangeGuidesSide()
        yield ChangeTheme()
        yield from self.maybe(CopyEntryTextToClipboard)
        yield from self.maybe(CopyEntrySourceToClipboard)
        yield Escape()
        yield from self.maybe(GoToNextEntry)
        yield from self.maybe(GoToParent)
        yield from self.maybe(GoToPreviousEntry)
        yield Help()
        yield JumpToMenu()
        yield Quit()
        yield from self.maybe(SaveEntrySource)
        yield from self.maybe(SaveEntryText)
        yield from self.maybe(SeeAlso)
        yield from self.maybe(SearchForGuide)
        yield ToggleClassicView()
        yield ToggleGuides()


### main.py ends here
