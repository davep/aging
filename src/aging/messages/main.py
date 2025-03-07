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


##############################################################################
@dataclass
class OpenEntry(Message):
    """Message that requests an entry be opened."""

    location: int
    """The location of the entry to open."""


### main.py ends here
