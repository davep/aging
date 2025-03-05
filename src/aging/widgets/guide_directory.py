"""Provides the guide directory widget."""

##############################################################################
# Textual enhanced imports.
from textual.reactive import var
from textual_enhanced.widgets import EnhancedOptionList

##############################################################################
# Local imports.
from ..data import Guides


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

    guides: var[Guides] = var(Guides)
    """The guides in the directory."""

    def _watch_guides(self) -> None:
        """React to the guides being changed."""
        with self.preserved_highlight:
            self.clear_options().add_options(guide.title for guide in self.guides)


### guide_directory.py ends here
