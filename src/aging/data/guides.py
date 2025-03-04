"""Provides a method of holding and storing the list of known guides."""

##############################################################################
# Backward compatibility.
from __future__ import annotations

##############################################################################
# Python imports.
from dataclasses import dataclass
from pathlib import Path
from typing import TypeAlias


##############################################################################
@dataclass(frozen=True)
class Guide:
    """Details of a Norton Guide that's registered with the application."""

    title: str
    """The title of the guide."""

    location: Path
    """The location of the guide."""

    @classmethod
    def from_json(cls, data: dict[str, str]) -> Guide:
        """Load a guide from some JSON data.

        Args:
            data: The data to load from.

        Returns:
            A fresh instance of a guide.
        """
        return cls(data.get("title", ""), Path(data.get("location", "")))

    @property
    def as_json(self) -> dict[str, str]:
        """The guide in a JSON-friendly format."""
        return {"title": self.title, "location": str(self.location)}


##############################################################################
Guides: TypeAlias = list[Guide]
"""The type of a collection of registered guides."""

### guides.py ends here
