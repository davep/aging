"""Provides the main commands for the application."""

##############################################################################
# Textual enhanced imports.
from textual_enhanced.commands import Command


##############################################################################
class ToggleGuides(Command):
    """Toggle the display of the guides directory panel"""

    BINDING_KEY = "g"
    SHOW_IN_FOOTER = True
    FOOTER_TEXT = "Guides"


##############################################################################
class SearchForGuide(Command):
    """Search for a guide in the directory and open it"""

    BINDING_KEY = "G"


##############################################################################
class ChangeGuidesSide(Command):
    """Change which side the guides directory loves on"""

    BINDING_KEY = "["


##############################################################################
class CopyEntryTextToClipboard(Command):
    """Copy the text of the current entry to the clipboard"""

    BINDING_KEY = "c"


##############################################################################
class CopyEntrySourceToClipboard(Command):
    """Copy the source of the current entry to the clipboard"""

    BINDING_KEY = "C"


##############################################################################
class SaveEntryText(Command):
    """Save the text of the current entry to a file."""

    BINDING_KEY = "s"


##############################################################################
class SaveEntrySource(Command):
    """Save the source of the current entry to a file."""

    BINDING_KEY = "S"


##############################################################################
class Escape(Command):
    """Back out of the application, depending on location and context"""

    BINDING_KEY = "escape"


##############################################################################
class JumpToMenu(Command):
    """Jump into the guide's menu"""

    BINDING_KEY = "m"


##############################################################################
class AboutTheGuide(Command):
    """View the about information for the current guide"""

    BINDING_KEY = "A"
    SHOW_IN_FOOTER = True
    FOOTER_TEXT = "About"


##############################################################################
class ToggleClassicView(Command):
    """Toggle the classic Norton Guide colour scheme in the entry viewer"""

    BINDING_KEY = "shift+f9"


##############################################################################
class BrowseForGuide(Command):
    """Browse the filesystem for a guide to view"""

    BINDING_KEY = "o"


### main.py ends here
