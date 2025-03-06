"""Provides the main commands for the application."""

##############################################################################
# Textual enhanced imports.
from textual_enhanced.commands import Command


##############################################################################
class ToggleGuides(Command):
    """Toggle the display of the guides directory panel"""

    BINDING_KEY = "f2"
    SHOW_IN_FOOTER = True
    FOOTER_TEXT = "Guides"


##############################################################################
class ChangeGuidesSide(Command):
    """Change which side the guides directory loves on"""

    BINDING_KEY = "shift+f2"


### main.py ends here
