"""Provides a method of holding results of a search."""

##############################################################################
# Python imports.
from pathlib import Path
from typing import NamedTuple, TypeAlias


##############################################################################
class SearchHit(NamedTuple):
    """Holds the details of a hit from a search."""

    guide: Path
    """The guide in which the hit was found."""
    entry_offset: int
    """The offset of the entry in which the hit was found."""
    entry_line: int
    """The number of the line in which the hit was found."""
    line_source: str
    """The guide source for the line in which the hit was found."""


##############################################################################
SearchHits: TypeAlias = list[SearchHit]
"""The type of a collection of search hits."""

### search_hits.py ends here
