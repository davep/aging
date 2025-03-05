"""The main messages for the application."""

##############################################################################
# Python imports.
from dataclasses import dataclass
from pathlib import Path

##############################################################################
# Textual imports.
from textual.message import Message


##############################################################################
@dataclass
class OpenGuide(Message):
    """Message that requests a guide be opened."""

    location: Path
    """The path to the file to open."""


### main.py ends here
