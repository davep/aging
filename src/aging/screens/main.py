"""Provides the main screen."""

##############################################################################
# Textual imports.
from textual.app import ComposeResult
from textual.containers import HorizontalGroup
from textual.reactive import var
from textual.widgets import Footer, Header

##############################################################################
# Textual enhanced imports.
from textual_enhanced.commands import ChangeTheme, Command, Help, Quit
from textual_enhanced.screen import EnhancedScreen

##############################################################################
# Local imports.
from .. import __version__
from ..data import Guides, load_guides
from ..providers import MainCommands
from ..widgets import EntryViewer, GuideDirectory


##############################################################################
class Main(EnhancedScreen[None]):
    """The main screen for the application."""

    TITLE = f"Aging v{__version__}"

    DEFAULT_CSS = """
    Main {
        layout: horizontal;

        .panel {
            background: $surface;
            &:focus-within {
                background: $panel 80%;
            }
            * {
                scrollbar-background: $surface;
                scrollbar-background-hover: $surface;
                scrollbar-background-active: $surface;
            }
            &:focus-within * {
                scrollbar-background: $panel;
                scrollbar-background-hover: $panel;
                scrollbar-background-active: $panel;
            }
        }

        #workspace {
            hatch: right $surface;
            .panel {
                border-left: solid $panel;
                &:focus, &:focus-within {
                    border-left: solid $border;
                }
            }
        }
    }
    """

    HELP = """
    ## Main application keys and commands

    The following key bindings and commands are available:
    """

    COMMAND_MESSAGES = (
        # Keep these together as they're bound to function keys and destined
        # for the footer.
        Help,
        ChangeTheme,
        Quit,
    )

    BINDINGS = Command.bindings(*COMMAND_MESSAGES)
    COMMANDS = {MainCommands}

    guides: var[Guides] = var(Guides)
    """The directory of Norton Guides."""

    def compose(self) -> ComposeResult:
        """Compose the content of the main screen."""
        yield Header()
        with HorizontalGroup(id="workspace"):
            yield GuideDirectory(classes="panel")
            yield EntryViewer(classes="panel")
        yield Footer()

    def on_mount(self) -> None:
        """Configure the screen once the DOM is mounted."""
        self.guides = load_guides()


### main.py ends here
