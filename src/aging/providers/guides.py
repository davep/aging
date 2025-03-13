"""Commands for opening a guide from the guide directory."""

##############################################################################
# Textual enhanced imports.
from textual_enhanced.commands import CommandHit, CommandHits, CommandsProvider

##############################################################################
# Local imports.
from ..data import Guides
from ..messages import OpenGuide


##############################################################################
class GuidesCommands(CommandsProvider):
    """A command palette provider for opening a guide from the directory."""

    guides = Guides()
    """The guides in the directory."""

    @classmethod
    def prompt(cls) -> str:
        """The prompt for the command provider."""
        return "Search the directory for a Norton Guide..."

    def commands(self) -> CommandHits:
        """Provide a list of commands for opening a specific Norton Guide.

        Yields:
            Commands to show in the command palette.
        """
        for guide in sorted(self.guides):
            yield CommandHit(
                f"{guide.title} ({guide.location.name})",
                f"Open and view {guide.location.name}",
                OpenGuide(guide.location),
            )


### guides.py ends here
