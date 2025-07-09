"""The main entry point to the application."""

##############################################################################
# Python imports.
from argparse import ArgumentParser, Namespace
from inspect import cleandoc
from operator import attrgetter
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

    # Add --bindings
    parser.add_argument(
        "-b",
        "--bindings",
        help="List commands that can have their bindings changed",
        action="store_true",
    )

    # An optional guide to open.
    parser.add_argument(
        "guide",
        nargs="?",
        type=Path,
        help="A guide to open",
    )

    # Finally, parse the command line.
    return parser.parse_args()


##############################################################################
def show_bindable_commands() -> None:
    """Show the commands that can have bindings applied."""
    from rich.console import Console
    from rich.markup import escape

    from .screens import Main

    console = Console(highlight=False)
    for command in sorted(Main.COMMAND_MESSAGES, key=attrgetter("__name__")):
        if command().has_binding:
            console.print(
                f"[bold]{escape(command.__name__)}[/] [dim italic]- {escape(command.tooltip())}[/]"
            )
            console.print(
                f"    [dim italic]Default: {escape(command.binding().key)}[/]"
            )


##############################################################################
def main() -> None:
    """Main entry function."""
    if (args := get_args()).license:
        print(cleandoc(AgiNG.HELP_LICENSE))
    elif args.bindings:
        show_bindable_commands()
    else:
        AgiNG(args).run()


##############################################################################
if __name__ == "__main__":
    main()

### __main__.py ends here
