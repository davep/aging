"""Provides a method of holding and storing the list of known guides."""

##############################################################################
# Backward compatibility.
from __future__ import annotations

##############################################################################
# Python imports.
from dataclasses import dataclass
from functools import total_ordering
from json import dumps, loads
from pathlib import Path
from typing import TypeAlias

##############################################################################
# Local imports.
from .locations import data_dir


##############################################################################
@dataclass(frozen=True)
@total_ordering
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

    def __gt__(self, value: object, /) -> bool:
        if isinstance(value, Guide):
            return self.title.casefold() > value.title.casefold()
        raise NotImplementedError

    def __eq__(self, value: object, /) -> bool:
        if isinstance(value, Guide):
            return self.title.casefold() == value.title.casefold()
        if isinstance(value, str):
            return self.title.casefold() == value.casefold()
        if isinstance(value, Path):
            return (
                isinstance(self.location, Path)
                and self.location.resolve() == value.resolve()
            )
        raise NotImplementedError


##############################################################################
Guides: TypeAlias = list[Guide]
"""The type of a collection of registered guides."""


##############################################################################
def guides_file() -> Path:
    """The path to the guides file.

    Returns:
        The path where the guides directory is held.
    """
    return data_dir() / "guides.json"


##############################################################################
def save_guides(guides: Guides) -> None:
    """Save the guide directory to storage.

    Args:
        guides: The guides to save.
    """
    guides_file().write_text(
        dumps([guide.as_json for guide in guides], indent=4), encoding="utf-8"
    )


##############################################################################
def load_guides() -> Guides:
    """Load the guide directory from storage.

    Returns:
        The guides in the directory.
    """
    return (
        [
            Guide.from_json(data)
            for data in loads(guides_file().read_text(encoding="utf-8"))
        ]
        if guides_file().exists()
        else []
    )


### guides.py ends here
