"""Provides functions and classes for managing the app's data."""

##############################################################################
# Local imports.
from .config import (
    Configuration,
    load_configuration,
    save_configuration,
    update_configuration,
)
from .guides import Guide, Guides, load_guides, save_guides

##############################################################################
# Exports.
__all__ = [
    "Configuration",
    "Guide",
    "Guides",
    "load_configuration",
    "load_guides",
    "save_configuration",
    "save_guides",
    "update_configuration",
]

### __init__.py ends here
