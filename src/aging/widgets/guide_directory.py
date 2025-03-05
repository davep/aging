"""Provides the guide directory widget."""

##############################################################################
# Textual enhanced imports.
from textual_enhanced.widgets import EnhancedOptionList


##############################################################################
class GuideDirectory(EnhancedOptionList):
    """A widget that holds and manages the Norton Guide directory."""

    DEFAULT_CSS = """
    GuideDirectory {
        width: 27%;
        min-width: 30;
        dock: left;
        background: transparent;
        height: 1fr;
        border: none;
        &:focus {
            border: none;
        }
    }
    """


### guide_directory.py ends here
