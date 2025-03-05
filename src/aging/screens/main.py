"""Provides the main screen."""

##############################################################################
# Python imports.
from pathlib import Path

##############################################################################
# NGDB imports.
from ngdb import NortonGuide, make_dos_like

##############################################################################
# Textual imports.
from textual import on, work
from textual.app import ComposeResult
from textual.containers import HorizontalGroup
from textual.reactive import var
from textual.widgets import Footer, Header

##############################################################################
# Textual enhanced imports.
from textual.worker import get_current_worker
from textual_enhanced.commands import ChangeTheme, Command, Help, Quit
from textual_enhanced.screen import EnhancedScreen

##############################################################################
# Textual fspicker imports.
from textual_fspicker import SelectDirectory

##############################################################################
# Local imports.
from .. import __version__
from ..commands import AddGuidesToDirectory
from ..data import Guide, Guides, load_guides, save_guides
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
        # The following don't need to be in a specific order.
        AddGuidesToDirectory,
    )

    BINDINGS = Command.bindings(*COMMAND_MESSAGES)
    COMMANDS = {MainCommands}

    guides: var[Guides] = var(Guides)
    """The directory of Norton Guides."""

    def compose(self) -> ComposeResult:
        """Compose the content of the main screen."""
        yield Header()
        with HorizontalGroup(id="workspace"):
            yield GuideDirectory(classes="panel").data_bind(Main.guides)
            yield EntryViewer(classes="panel")
        yield Footer()

    def on_mount(self) -> None:
        """Configure the screen once the DOM is mounted."""
        self.guides = load_guides()

    def _new_guides(self, guides: Guides) -> None:
        """Add a list of new guides to the guide directory.

        Args:
            guides: The new guides to add.
        """
        # Try and ensure we don't get duplicates based on location;
        # duplicates based on title are fine and it's up to the user to
        # decide if they want to remove them or not.
        guides = [guide for guide in guides if guide.location not in self.guides]
        if guides:
            self.guides = sorted(self.guides + guides)
            save_guides(self.guides)
            self.notify(f"New guides scanned and added: {len(guides)}")
        else:
            self.notify("No new guides found", severity="warning")

    @work(thread=True)
    def _add_guides_from(self, directory: Path) -> None:
        """Add guides in a directory to the directory of guides.

        Args:
            directory: The directory to scan for Norton Guides.
        """
        worker = get_current_worker()
        guides: list[Guide] = []
        for candidate in directory.glob("**/*.*"):
            if worker.is_cancelled:
                return
            if candidate.suffix.lower() == ".ng":
                with NortonGuide(candidate) as guide:
                    if guide.is_a:
                        guides.append(Guide(make_dos_like(guide.title), guide.path))
        if guides:
            self.app.call_from_thread(self._new_guides, guides)

    @on(AddGuidesToDirectory)
    @work
    async def action_add_guides_to_directory_command(self) -> None:
        """Let the user add more guides to the guide directory."""
        if add_from := await self.app.push_screen_wait(
            SelectDirectory(title="Add Norton Guides From...")
        ):
            self._add_guides_from(add_from)


### main.py ends here
