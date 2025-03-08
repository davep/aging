"""Provides application commands related to guide navigation."""

##############################################################################
# Textual enhanced imports.
from textual_enhanced.commands import Command


##############################################################################
class GoToPreviousEntry(Command):
    """Navigate to the previous entry"""

    BINDING_KEY = "ctrl+left"
    SHOW_IN_FOOTER = True
    FOOTER_TEXT = "Prev"


##############################################################################
class GoToNextEntry(Command):
    """Navigate to the next entry"""

    BINDING_KEY = "ctrl+right"
    SHOW_IN_FOOTER = True
    FOOTER_TEXT = "Next"


### guide_navigation.py ends here
