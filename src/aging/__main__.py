"""The main entry point to the application."""

##############################################################################
# Local imports.
from .aging import Aging

##############################################################################
def main() -> None:
    """Main entry function."""
    Aging().run()

##############################################################################
if __name__ == "__main__":
    main()

### __main__.py ends here
