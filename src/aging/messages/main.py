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

    initial_offset: int | None = None
    """The optional offset of an entry to open once the guide is opened."""


##############################################################################
@dataclass
class OpenEntry(Message):
    """Message that requests an entry be opened."""

    location: int
    """The location of the entry to open."""

    initial_line: int | None = None
    """The optional line to highlight once the entry is opened."""


##############################################################################
class GuidesUpdated(Message):
    """Message sent when the guide directory has been updated."""


### main.py ends here
