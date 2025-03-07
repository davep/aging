"""Provides the main screen."""

##############################################################################
# Python imports.
from pathlib import Path

##############################################################################
# NGDB imports.
from ngdb import Entry, NortonGuide, PlainText, make_dos_like

##############################################################################
# Pyperclip imports.
from pyperclip import PyperclipException
from pyperclip import copy as copy_to_clipboard

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
from ..commands import (
    AddGuidesToDirectory,
    ChangeGuidesSide,
    CopyEntrySourceToClipboard,
    CopyEntryToClipboard,
    ToggleGuides,
)
from ..data import (
    Guide,
    Guides,
    load_configuration,
    load_guides,
    save_guides,
    update_configuration,
)
from ..messages import CopyToClipboard, OpenEntry, OpenGuide
from ..providers import MainCommands
from ..widgets import EntryViewer, GuideDirectory, GuideMenu


##############################################################################
class Main(EnhancedScreen[None]):
    """The main screen for the application."""

    TITLE = f"Aging v{__version__}"

    DEFAULT_CSS = """
    Main {
        layout: horizontal;

        #workspace {
            width: 1fr;
            height: 1fr;
            hatch: right $surface;
            .panel {
                border-left: solid $panel;
                &:focus, &:focus-within {
                    border-left: solid $border;
                }
            }
        }

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

        GuideDirectory {
            display: none;
        }
        &.guides GuideDirectory {
            display: block;
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
        ToggleGuides,
        ChangeTheme,
        Quit,
        # The following don't need to be in a specific order.
        AddGuidesToDirectory,
        ChangeGuidesSide,
        CopyEntryToClipboard,
        CopyEntrySourceToClipboard,
    )

    BINDINGS = Command.bindings(*COMMAND_MESSAGES)
    COMMANDS = {MainCommands}

    guides: var[Guides] = var(Guides)
    """The directory of Norton Guides."""

    current_guide: var[NortonGuide | None] = var(None)
    """The currently-opened Norton Guide."""

    current_entry: var[Entry | None] = var(None)
    """The entry that is being currently viewed."""

    guides_visible: var[bool] = var(True)
    """Should the guides directory be visible?"""

    guides_on_right: var[bool] = var(False, init=False)
    """Should the guides directory be docked to the right?"""

    def compose(self) -> ComposeResult:
        """Compose the content of the main screen."""
        yield Header()
        with HorizontalGroup(id="workspace"):
            yield GuideDirectory(classes="panel").data_bind(
                Main.guides, dock_right=Main.guides_on_right
            )
            yield GuideMenu(classes="panel").data_bind(guide=Main.current_guide)
            yield EntryViewer(classes="panel").data_bind(entry=Main.current_entry)
        yield Footer()

    def _watch_current_guide(self) -> None:
        """React to the current guide being changed."""
        if self.current_guide is None:
            self.sub_title = ""
            self.current_entry = None
        else:
            self.sub_title = self.current_guide.title
            self.current_entry = self.current_guide.load()

    def _watch_guides_visible(self) -> None:
        """React to the guides directory viability flag being changed."""
        self.set_class(self.guides_visible, "guides")
        with update_configuration() as config:
            config.guides_directory_visible = self.guides_visible

    def _watch_guides_on_right(self) -> None:
        """React to the guides location being changed."""
        with update_configuration() as config:
            config.guides_directory_on_right = self.guides_on_right

    def on_mount(self) -> None:
        """Configure the screen once the DOM is mounted."""
        self.guides = load_guides()
        config = load_configuration()
        self.guides_visible = config.guides_directory_visible
        self.guides_on_right = config.guides_directory_on_right

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

    def check_action(self, action: str, parameters: tuple[object, ...]) -> bool | None:
        """Check if an action is possible to perform right now.

        Args:
            action: The action to perform.
            parameters: The parameters of the action.

        Returns:
            `True` if it can perform, `False` or `None` if not.
        """
        if not self.is_mounted:
            # Surprisingly it seems that Textual's "dynamic bindings" can
            # cause this method to be called before the DOM is up and
            # running. This breaks the rule of least astonishment, I'd say,
            # but okay let's be defensive... (when I can come up with a nice
            # little MRE I'll report it).
            return True
        if action in (
            command.action_name()
            for command in (CopyEntryToClipboard, CopyEntrySourceToClipboard)
        ):
            return self.current_entry is not None
        return True

    @on(AddGuidesToDirectory)
    @work
    async def action_add_guides_to_directory_command(self) -> None:
        """Let the user add more guides to the guide directory."""
        if add_from := await self.app.push_screen_wait(
            SelectDirectory(title="Add Norton Guides From...")
        ):
            self._add_guides_from(add_from)

    @on(OpenGuide)
    def _open_guide(self, message: OpenGuide) -> None:
        """Handle a request to open a guide.

        Args:
            message: The message requesting a guide be opened.
        """
        # TO start with, let's be sure that the guide is there and it
        # actually is a guide.
        try:
            new_guide = NortonGuide(message.location)
        except IOError as error:
            self.notify(
                str(error), title=f"Error opening {message.location}", severity="error"
            )
            return
        if not (new_guide := NortonGuide(message.location)).is_a:
            self.notify(
                "That file doesn't appear to be a valid Norton Guide",
                title=str(message.location),
                severity="error",
            )
            return

        # If there is a guide already open, ensure it gets closed.
        if self.current_guide is not None:
            self.current_guide.close()

        # Looks good.
        self.current_guide = new_guide

    @on(OpenEntry)
    def _open_entry(self, message: OpenEntry) -> None:
        """Handle a request to open an entry.

        Args:
            message: The message requesting an entry be opened.
        """
        if self.current_guide is not None:
            self.current_entry = self.current_guide.goto(message.location).load()

    @on(ToggleGuides)
    def action_toggle_guides_command(self) -> None:
        """Toggle the display of the guides panel."""
        self.guides_visible = not self.guides_visible

    @on(ChangeGuidesSide)
    def action_change_guides_side_command(self) -> None:
        """Change which side the guides directory is docked to."""
        self.guides_on_right = not self.guides_on_right

    @on(CopyToClipboard)
    def _copy_text_to_clipbaord(self, message: CopyToClipboard) -> None:
        """Copy some text into the clipboard.

        Args:
            message: The message requesting the text be copied.
        """
        # First off, use Textual's own copy to clipboard facility. Generally
        # this will work in most terminals, and if it does it'll likely work
        # best, getting the text through remote connections to the user's
        # own environment.
        self.app.copy_to_clipboard(message.text)
        # However, as a backup, use pyerclip too. If the above did fail due
        # to the terminal not supporting the operation, this might.
        try:
            copy_to_clipboard(message.text)
        except PyperclipException:
            pass
        # Give the user some feedback.
        self.notify("Copied")

    @on(CopyEntryToClipboard)
    def action_copy_entry_to_clipboard_command(self) -> None:
        """Copy the text of the current entry to the clipboard."""
        if self.current_entry is not None:
            self.post_message(
                CopyToClipboard(
                    "\n".join(
                        make_dos_like(str(PlainText(line)))
                        for line in self.current_entry.lines
                    )
                )
            )

    @on(CopyEntrySourceToClipboard)
    def action_copy_entry_source_to_clipboard_command(self) -> None:
        """Copy the source of the current entry to the clipboard."""
        if self.current_entry is not None:
            self.post_message(CopyToClipboard(make_dos_like(str(self.current_entry))))


### main.py ends here
