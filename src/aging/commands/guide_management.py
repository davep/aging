"""Provides commands related to guide management."""

##############################################################################
# Textual enhanced imports.
from textual_enhanced.commands import Command


##############################################################################
class AddGuidesToDirectory(Command):
    """Scan a sub-directory for Norton Guide files to add to the directory"""

    BINDING_KEY = "D"


### guide_management.py ends here
