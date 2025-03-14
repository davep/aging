"""Provides the main screen."""

##############################################################################
# Python imports.
from argparse import Namespace
from pathlib import Path
from typing import Iterator

##############################################################################
# NGDB imports.
from ngdb import Long, NGDBError, NortonGuide, PlainText, Short, make_dos_like

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
from textual_fspicker import FileOpen, FileSave, Filters, SelectDirectory

##############################################################################
# Local imports.
from .. import __version__
from ..commands import (
    AboutTheGuide,
    AddGuidesToDirectory,
    BrowseForGuide,
    ChangeGuidesSide,
    CopyEntrySourceToClipboard,
    CopyEntryTextToClipboard,
    Escape,
    GoToNextEntry,
    GoToParent,
    GoToPreviousEntry,
    JumpToMenu,
    SaveEntrySource,
    SaveEntryText,
    SearchForGuide,
    SeeAlso,
    ToggleClassicView,
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
from ..messages import CopyToClipboard, GuidesUpdated, OpenEntry, OpenGuide
from ..providers import GuidesCommands, MainCommands
from ..widgets import EntryViewer, GuideDirectory, GuideMenu
from .about import About


##############################################################################
class Main(EnhancedScreen[None]):
    """The main screen for the application."""

    TITLE = f"AgiNG v{__version__}"

    DEFAULT_CSS = """
    Main {
        layout: horizontal;

        #workspace {
            width: 1fr;
            height: 1fr;
            hatch: right $surface;
            .panel {
                border-left: solid $panel;
                background: $surface;
                &:focus, &:focus-within {
                    border-left: solid $border;
                    background: $panel 80%;
                }
            }
        }

        GuideDirectory {
            display: none;
            min-width: 20%;
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
        AboutTheGuide,
        SeeAlso,
        GoToPreviousEntry,
        GoToParent,
        GoToNextEntry,
        Quit,
        # The following don't need to be in a specific order.
        AddGuidesToDirectory,
        ChangeGuidesSide,
        ChangeTheme,
        CopyEntrySourceToClipboard,
        CopyEntryTextToClipboard,
        Escape,
        JumpToMenu,
        ToggleClassicView,
        BrowseForGuide,
        SearchForGuide,
        SaveEntrySource,
        SaveEntryText,
    )

    BINDINGS = Command.bindings(*COMMAND_MESSAGES)
    COMMANDS = {MainCommands}

    guides: var[Guides] = var(Guides)
    """The directory of Norton Guides."""

    guide: var[NortonGuide | None] = var(None, init=False)
    """The currently-opened Norton Guide."""

    entry: var[Short | Long | None] = var(None, init=False)
    """The entry that is being currently viewed."""

    guides_visible: var[bool] = var(True)
    """Should the guides directory be visible?"""

    guides_on_right: var[bool] = var(False, init=False)
    """Should the guides directory be docked to the right?"""

    classic_view: var[bool] = var(False, init=False)
    """Should the entry viewer use a classic Norton Guide colour scheme?"""

    def __init__(self, arguments: Namespace) -> None:
        """Initialise the main screen.

        Args:
            arguments: The arguments passed to the application on the command line.
        """
        self._arguments = arguments
        """The arguments passed on the command line."""
        super().__init__()

    def compose(self) -> ComposeResult:
        """Compose the content of the main screen."""
        yield Header()
        with HorizontalGroup(id="workspace"):
            yield GuideDirectory(classes="panel").data_bind(
                Main.guides, Main.guide, dock_right=Main.guides_on_right
            )
            yield GuideMenu(classes="panel").data_bind(Main.guide, Main.entry)
            yield EntryViewer(classes="panel").data_bind(Main.entry, Main.classic_view)
        yield Footer()

    @property
    def entry_path(self) -> Iterator[str]:
        """Generate the path for the current entry.

        Yields:
            The main path towards the current entry.
        """
        if self.guide is None:
            return
        yield self.guide.path.name
        yield make_dos_like(self.guide.title)
        if self.entry is not None:
            if self.entry.parent.has_menu:
                yield make_dos_like(self.guide.menus[self.entry.parent.menu].title)
            if self.entry.parent.has_prompt:
                yield make_dos_like(
                    self.guide.menus[self.entry.parent.menu].prompts[
                        self.entry.parent.prompt
                    ]
                )

    def _refresh_sub_title(self) -> None:
        """Refresh the subtitle of the window."""
        self.sub_title = " » ".join(self.entry_path)

    def _watch_guides(self) -> None:
        """React to the list of guides being changed."""
        GuidesCommands.guides = self.guides

    def _watch_guides_visible(self) -> None:
        """React to the guides directory viability flag being changed."""
        self.set_class(self.guides_visible, "guides")
        with update_configuration() as config:
            config.guides_directory_visible = self.guides_visible

    def _watch_classic_view(self) -> None:
        """React to the classic view being changed."""
        with update_configuration() as config:
            config.classic_view = self.classic_view

    def _watch_guides_on_right(self) -> None:
        """React to the guides location being changed."""
        with update_configuration() as config:
            config.guides_directory_on_right = self.guides_on_right

    def _watch_guide(self) -> None:
        """React to the current guide being changed."""
        with update_configuration() as config:
            config.current_guide = None if self.guide is None else str(self.guide.path)
        # The guide has changed, so let's nuke whatever entry we were
        # viewing.
        self.entry = None
        if self.guide is not None:
            # We loaded a guide, so let's try and load and display the entry
            # at the current location -- we might have been set up elsewhere
            # to load a specific entry.
            try:
                self.entry = self.guide.load()
            except NGDBError:
                # There's no reason why the above load should have failed;
                # but if we have failed it's possibly because we were trying
                # to load up an entry we were last viewing before, and
                # something about the guide has changed, so as a last resort
                # let's try and go with the first entry.
                try:
                    self.entry = self.guide.goto_first().load()
                except NGDBError as error:
                    self.notify(
                        str(error), title="Failed to load an entry", severity="error"
                    )
        self._refresh_sub_title()

    def _watch_entry(self) -> None:
        """React to the current entry being changed."""
        with update_configuration() as config:
            config.current_entry = None if self.entry is None else self.entry.offset
        self._refresh_sub_title()
        self.refresh_bindings()

    def on_mount(self) -> None:
        """Configure the screen once the DOM is mounted."""
        self.guides = load_guides()
        config = load_configuration()
        self.guides_visible = config.guides_directory_visible
        self.guides_on_right = config.guides_directory_on_right
        self.classic_view = config.classic_view
        if self._arguments.guide:
            self.post_message(OpenGuide(self._arguments.guide))
        elif config.current_guide:
            self.post_message(
                OpenGuide(Path(config.current_guide), config.current_entry)
            )
        if not self.guides_visible:
            self.set_focus(self.query_one(GuideMenu))

    def _new_guides(self, guides: Guides) -> None:
        """Add a list of new guides to the guide directory.

        Args:
            guides: The new guides to add.
        """
        # Try and ensure we don't get duplicates based on location;
        # duplicates based on title are fine and it's up to the user to
        # decide if they want to remove them or not.
        if guides := [guide for guide in guides if guide.location not in self.guides]:
            self.guides = self.guides + guides
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
        with update_configuration() as config:
            config.last_added_guides_from = str(directory.resolve())
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
        if action == GoToNextEntry.action_name():
            return self.entry is not None and self.entry.has_next or None
        if action == GoToPreviousEntry.action_name():
            return self.entry is not None and self.entry.has_previous or None
        if action == GoToParent.action_name():
            return self.entry is not None and bool(self.entry.parent) or None
        if action == SeeAlso.action_name():
            if isinstance(self.entry, Long):
                return self.entry.has_see_also or None
            return False
        if action == SearchForGuide.action_name():
            return bool(self.guides)
        if action == AboutTheGuide.action_name():
            return bool(self.guide) or None
        if action in (
            command.action_name()
            for command in (
                CopyEntryTextToClipboard,
                CopyEntrySourceToClipboard,
                SaveEntryText,
                SaveEntrySource,
            )
        ):
            return self.entry is not None
        return True

    @on(GuidesUpdated)
    def _reload_guides(self) -> None:
        """Reaload the guide directory from storage."""
        self.guides = load_guides()

    @on(AddGuidesToDirectory)
    @work
    async def action_add_guides_to_directory_command(self) -> None:
        """Let the user add more guides to the guide directory."""
        if add_from := await self.app.push_screen_wait(
            SelectDirectory(
                Path(load_configuration().last_added_guides_from),
                title="Add Norton Guides From...",
            )
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
        if self.guide is not None:
            self.guide.close()

        # If we're being asked to jump to a specific entry, to start with,
        # make sure we're there...
        if message.initial_offset is not None:
            new_guide.goto(message.initial_offset)

        # Looks good.
        self.guide = new_guide

        # Having opening the guide, the user probably wants to be in the
        # menu.
        self.query_one(GuideMenu).focus()

    @on(OpenEntry)
    def _open_entry(self, message: OpenEntry) -> None:
        """Handle a request to open an entry.

        Args:
            message: The message requesting an entry be opened.
        """
        if self.guide is not None:
            self.entry = self.guide.goto(message.location).load()
            if message.initial_line is not None:
                self.query_one(EntryViewer).goto_line(message.initial_line)
            self.query_one(EntryViewer).focus()

    @on(ToggleGuides)
    def action_toggle_guides_command(self) -> None:
        """Toggle the display of the guides panel."""
        self.guides_visible = not self.guides_visible
        if self.guides_visible:
            # If the directory has been made visible it's almost always
            # going to be because the user wants to interact with it; so
            # send focus there.
            self.set_focus(self.query_one(GuideDirectory))

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
        self.notify(f"Copied {message.description or ''}".strip())

    @property
    def _entry_text(self) -> str:
        """The text of the current entry."""
        return (
            ""
            if self.entry is None
            else "\n".join(
                make_dos_like(str(PlainText(line))) for line in self.entry.lines
            )
        )

    @property
    def _entry_source(self) -> str:
        """The source of the current entry."""
        return (
            ""
            if self.entry is None
            else "\n".join(make_dos_like(line) for line in self.entry.lines)
        )

    @on(CopyEntryTextToClipboard)
    def action_copy_entry_text_to_clipboard_command(self) -> None:
        """Copy the text of the current entry to the clipboard."""
        if self.entry is not None:
            self.post_message(CopyToClipboard(self._entry_text, "the entry's text"))

    @on(CopyEntrySourceToClipboard)
    def action_copy_entry_source_to_clipboard_command(self) -> None:
        """Copy the source of the current entry to the clipboard."""
        if self.entry is not None:
            self.post_message(CopyToClipboard(self._entry_source, "the entry's source"))

    async def _save_entry(self, content: str, content_type: str) -> None:
        """Save an entry's content to a file.

        Args:
            content: The content to save.
            content_type: A description of the type of content.
        """
        if self.entry is None:
            return
        if (
            text_file := await self.app.push_screen_wait(
                FileSave(title=f"Save {content_type} as...")
            )
        ) is not None:
            try:
                text_file.write_text(content, encoding="utf-8")
            except OSError as error:
                self.notify(str(error), title="Save error", severity="error")
                return
            self.notify(str(text_file), title=f"Entry {content_type} saved")

    @on(SaveEntrySource)
    @work
    async def action_save_entry_source_command(self) -> None:
        """Save the current entry's text to a file."""
        await self._save_entry(self._entry_source, "source")

    @on(SaveEntryText)
    @work
    async def action_save_entry_text_command(self) -> None:
        """Save the current entry's text to a file."""
        await self._save_entry(self._entry_text, "text")

    @on(GoToNextEntry)
    def action_go_to_next_entry_command(self) -> None:
        """Navigate to the next entry if there is one."""
        if self.entry is not None and self.entry.has_next:
            self.post_message(OpenEntry(self.entry.next))

    @on(GoToPreviousEntry)
    def action_go_to_previous_entry_command(self) -> None:
        """Navigate to the previous entry if there is one."""
        if self.entry is not None and self.entry.has_previous:
            self.post_message(OpenEntry(self.entry.previous))

    @on(GoToParent)
    def action_go_to_parent_command(self) -> None:
        """Navigate to the parent entry, if there s one."""
        if self.entry is not None and self.entry.parent:
            self.post_message(
                OpenEntry(
                    self.entry.parent.offset,
                    self.entry.parent.line if self.entry.parent.has_line else None,
                )
            )

    @on(Escape)
    def action_escape_command(self) -> None:
        """Handle the user bouncing on the escape key."""
        if self.focused is None:
            return
        if self.focused == self.query_one(GuideDirectory):
            # Escape in directory is always quit the app.
            self.app.exit()
        elif self.focused == self.query_one(GuideMenu):
            if self.guides_visible:
                # Escape in the menu, but the guides are visible, means
                # bounce out to the guides.
                self.set_focus(self.query_one(GuideDirectory))
            else:
                # The guides aren't visible, so escape in the menu is leave
                # the app.
                self.app.exit()
        elif self.query_one(EntryViewer).seeing_also:
            # We're in the viewer, but within the see-also section, so back
            # up to the main content.
            self.query_one(EntryViewer).focus()
        elif self.entry is not None:
            if self.entry.parent:
                # There's an entry and a parent, so that means back up to
                # the parent.
                self.post_message(GoToParent())
            else:
                # There's an entry without a parent, which implies it's the
                # top-level, so we bounce out the menu because the user
                # likely wants to navigate to another menu option.
                self.set_focus(self.query_one(GuideMenu))

    @on(SeeAlso)
    def action_see_also_command(self) -> None:
        """Show a menu of see-also entries."""
        self.query_one(EntryViewer).see_also()

    @on(JumpToMenu)
    def action_jump_to_menu_command(self) -> None:
        """Jump to the menu."""
        self.query_one(GuideMenu).focus()

    @on(AboutTheGuide)
    def action_about_the_guide_command(self) -> None:
        """Show details about the guide."""
        if self.guide is not None:
            self.app.push_screen(About(self.guide))

    @on(ToggleClassicView)
    def action_toggle_classic_view_command(self) -> None:
        """Toggle the classic view of the guide entry."""
        self.classic_view = not self.classic_view

    @on(BrowseForGuide)
    @work
    async def action_browse_for_guide_command(self) -> None:
        """Browse the filesystem for a guide to view"""
        if (
            guide := await self.app.push_screen_wait(
                FileOpen(
                    Path(load_configuration().last_opened_guide_from),
                    filters=Filters(
                        ("Norton Guides", lambda p: p.suffix.lower() == ".ng")
                    ),
                )
            )
        ) is not None:
            self.post_message(OpenGuide(guide))
            with update_configuration() as config:
                config.last_opened_guide_from = str(guide.parent)

    @on(SearchForGuide)
    def action_search_for_guide_command(self) -> None:
        """Search the directory for a guide and view it."""
        self.show_palette(GuidesCommands)


### main.py ends here
