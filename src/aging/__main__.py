"""The main entry point to the application."""

##############################################################################
# Local imports.
from .aging import AgiNG


##############################################################################
def main() -> None:
    """Main entry function."""
    AgiNG().run()


##############################################################################
if __name__ == "__main__":
    main()

### __main__.py ends here
