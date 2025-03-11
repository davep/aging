"""The main entry point to the application."""

##############################################################################
# Python imports.
from argparse import ArgumentParser, Namespace
from inspect import cleandoc
from pathlib import Path

##############################################################################
# Local imports.
from . import __doc__, __version__
from .aging import AgiNG


##############################################################################
def get_args() -> Namespace:
    """Get the command line arguments.

    Returns:
        The arguments.
    """

    # Build the parser.
    parser = ArgumentParser(
        prog="aging",
        description=__doc__,
        epilog=f"v{__version__}",
    )

    # Add --version
    parser.add_argument(
        "-v",
        "--version",
        help="Show version information",
        action="version",
        version=f"%(prog)s v{__version__}",
    )

    # Add --license
    parser.add_argument(
        "--license",
        "--licence",
        help="Show license information",
        action="store_true",
    )

    # An option guide to open.
    parser.add_argument(
        "guide",
        nargs="?",
        type=Path,
        help="A guide to open",
    )

    # Finally, parse the command line.
    return parser.parse_args()


##############################################################################
def main() -> None:
    """Main entry function."""
    if (args := get_args()).license:
        print(cleandoc(AgiNG.HELP_LICENSE))
    else:
        AgiNG(args).run()


##############################################################################
if __name__ == "__main__":
    main()

### __main__.py ends here
