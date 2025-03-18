"""Provides the search screen."""

##############################################################################
# NGDB imports.
from dataclasses import dataclass
from typing import Iterator

##############################################################################
# NGDB imports
from ngdb import Long, NGDBError, NortonGuide, PlainText, Short, make_dos_like

##############################################################################
# Textual imports.
from textual import on, work
from textual.app import ComposeResult
from textual.containers import HorizontalGroup, VerticalGroup
from textual.message import Message
from textual.reactive import var
from textual.screen import ModalScreen
from textual.widgets import Button, Checkbox, Input, Label, ProgressBar, Rule
from textual.worker import Worker, get_current_worker

##############################################################################
# Textual enhanced imports.
from textual_enhanced.widgets import EnhancedOptionList

##############################################################################
# Local imports.
from ..data.guides import Guide, Guides


##############################################################################
class SearchResults(EnhancedOptionList):
    """A widget that shows the search results."""

    DEFAULT_CSS = """
    SearchResults {
        height: 1fr;
        &, &:focus {
            background: transparent;
            border: none;
        }
    }
    """


##############################################################################
class Search(ModalScreen[None]):
    """Provides the global search screen."""

    DEFAULT_CSS = """
    Search {
        align: center middle;

        &> VerticalGroup {
            width: 80%;
            height: 80%;
            background: $panel;
            border: solid $border;

            &> HorizontalGroup {
                Input {
                    width: 1fr;
                }
            }
        }

        Rule {
            margin: 0 !important;
        }

        ProgressBar Bar {
            width: 1fr;
        }

        .--when-running {
            display: none;
        }
        .--when-stopped {
            display: block;
        }
        &.--running {
            .--when-running {
                display: block;
            }
            .--when-stopped {
                display: none;
            }
        }
    }
    """

    BINDINGS = [("escape", "dismiss(None)")]

    _search_running: var[bool] = var(False)
    """Are we searching?"""

    def __init__(self, guides: Guides, guide: NortonGuide | None) -> None:
        """Initialise the search screen.

        Args:
            guides: All the guides known to the application.
            guide: The current guide.
        """
        self._guides = guides
        """All the guides known to the application."""
        self._guide = guide
        """The current guide, if here is one."""
        super().__init__()

    def compose(self) -> ComposeResult:
        """Compose the content of the screen."""
        with VerticalGroup() as dialog:
            dialog.border_title = "Global Search"
            with HorizontalGroup():
                yield Input(placeholder="Search...")
                yield Checkbox("Global", True, id="global")
                yield Checkbox("Ignore Case", True, id="ignore_case")
                yield Button("Go", variant="primary", id="go", classes="--when-stopped")
                yield Button(
                    "Stop", variant="error", id="stop", classes="--when-running"
                )
            yield Rule(classes="--when-running")
            yield Label(id="current_guide", classes="--when-running", markup=False)
            yield ProgressBar(id="guides_progress", classes="--when-running")
            yield Label(id="current_entry", classes="--when-running", markup=False)
            yield ProgressBar(id="guide_progress", classes="--when-running")
            yield Rule()
            yield SearchResults(disabled=True, markup=False)

    def _watch__search_running(self) -> None:
        """React to the searching state changing."""
        self.set_class(self._search_running, "--running")
        for widget in self.query("Input, Checkbox"):
            widget.disabled = self._search_running

    @dataclass
    class Started(Message):
        """Message sent when a search has started."""

        searching: int
        """The number of guides we'll be searching."""

    class Ended(Message):
        """Message sent when the search has ended."""

    class Cancelled(Message):
        """Message sent when the search has been cancelled."""

    @dataclass
    class NewGuide(Message):
        """Message sent when a new guide is being searched."""

        position: int
        """The position of the guide in the list of guides to search."""
        guide: Guide
        """The information about the guide being searched."""

    @dataclass
    class NewEntry(Message):
        """Message sent when a new entry is being searched."""

        guide: NortonGuide
        """The guide being searched."""
        entry: Short | Long
        """The entry being searched."""

    @dataclass
    class NewMatch(Message):
        """Message sent when a new match is found in a guide entry."""

        guide: NortonGuide
        """The guide being searched."""
        entry: Short | Long
        """The entry being searched."""
        line_number: int
        """The number of the line where the match was found."""
        found_line: str
        """The text of the line that the match was found in."""

    class FinishedGuide(Message):
        """Message sent when we've finished searching a guide."""

    @on(Started)
    def _search_started(self, starting: Started) -> None:
        """Handle a search starting.

        Args:
            starting: The message that signals that a search has started.
        """
        self._search_running = True
        self.query_one("#guides_progress", ProgressBar).total = starting.searching

    @on(Ended)
    @on(Cancelled)
    def _search_ended(self) -> None:
        """Handle the search ending."""
        self._search_running = False

    @on(NewGuide)
    def _update_current_guide(self, current: NewGuide) -> None:
        """Handle the a new guide being searched.

        Args:
            current: The message that signals that a new guide is being searched.
        """
        self.query_one("#current_guide", Label).update(
            f"Searching {current.guide.title}"
        )
        self.query_one("#guides_progress", ProgressBar).progress = current.position
        self.query_one(
            "#guide_progress", ProgressBar
        ).total = current.guide.location.stat().st_size

    def _entry_description(
        self, guide: NortonGuide, entry: Short | Long
    ) -> Iterator[str]:
        """Generate a description for the given entry.

        Args:
            guide: The guide that is being searched.
            entry: The entry that is being searched.

        Yields:
            Parts of a description for the entry.
        """
        yield entry.__class__.__name__
        if entry.parent.has_menu:
            yield make_dos_like(guide.menus[entry.parent.menu].title)
        if entry.parent.has_prompt:
            yield make_dos_like(
                guide.menus[entry.parent.menu].prompts[entry.parent.prompt]
            )
        if first_non_empty_line := (
            next((line for line in entry if line.strip()), "")
            if isinstance(entry, Long)
            else next((line.text for line in entry if line.text.strip()), "")
        ):
            yield make_dos_like(str(PlainText(first_non_empty_line)))

    @on(NewEntry)
    def _update_current_entry(self, current: NewEntry) -> None:
        """Handle a new entry being searched.

        Args:
            current: The message that signals a new entry is being searched.
        """
        self.query_one("#current_entry", Label).update(
            " » ".join(self._entry_description(current.guide, current.entry))
        )
        self.query_one("#guide_progress", ProgressBar).progress = current.entry.offset

    @on(NewMatch)
    def _new_match_found(self, match: NewMatch) -> None:
        """Handle a new match being found.

        Args:
            match: The message that signals a match was found.
        """
        (hits := self.query_one(SearchResults)).disabled = False
        with hits.preserved_highlight:
            hits.add_option(
                make_dos_like(f"{match.guide.path.name} - {match.found_line}")
            )

    @on(FinishedGuide)
    def _finished_guide(self) -> None:
        """Handle a guide search finishing."""
        self.query_one("#current_entry", Label).update("Finished")
        if (total := self.query_one("#guide_progress", ProgressBar).total) is not None:
            self.query_one("#guide_progress", ProgressBar).progress = total

    def _search_entry(
        self,
        guide: NortonGuide,
        entry: Long | Short,
        worker: Worker[None],
        needle: str,
        ignore_case: bool,
    ) -> None:
        """Search within an entry.

        Args:
            entry: The entry to search.
            worker: The worker that we're working within.
            needle: The text to search for.
            ignore_case: Should case be ignored?
        """
        self.post_message(self.NewEntry(guide, entry))
        for line_number, line in enumerate(entry):
            if worker.is_cancelled:
                return
            haystack = found_line = str(PlainText(str(line)))
            if ignore_case:
                haystack = haystack.casefold()
            if needle in haystack:
                self.post_message(self.NewMatch(guide, entry, line_number, found_line))

    def _search_guide(
        self, guide: Guide, worker: Worker[None], needle: str, ignore_case: bool
    ) -> None:
        """Search within the given guide.

        Args:
            guide: The guide being searched.
            worker: The worker that we're working within.
            needle: The text to search for.
            ignore_case: Should case be ignored?
        """
        try:
            with NortonGuide(guide.location) as search:
                for entry in search:
                    if worker.is_cancelled:
                        return
                    self._search_entry(search, entry, worker, needle, ignore_case)
            self.post_message(self.FinishedGuide())
        except (IOError, NGDBError) as error:
            self.notify(
                str(error), title=f"Failed to search {guide.location}", severity="error"
            )

    @work(thread=True, exclusive=True, group="search")
    def _search(self, guides: Guides, needle: str, ignore_case: bool) -> None:
        """Start a new search.

        Args:
            guides: The guides to search.
            needle: The text to search for.
            ignore_case: Should case be ignored?
        """
        worker = get_current_worker()
        needle = needle.casefold() if ignore_case else needle
        self.post_message(self.Started(len(guides)))
        for position, guide in enumerate(sorted(guides)):
            if worker.is_cancelled:
                self.post_message(self.Cancelled())
                return
            self.post_message(self.NewGuide(position + 1, guide))
            self._search_guide(guide, worker, needle, ignore_case)
        self.post_message(self.Ended())

    @on(Input.Submitted)
    @on(Button.Pressed, "#go")
    def search(self) -> None:
        """React to a request to start a search."""
        if not self.query_one(Input).value.strip():
            self.notify(
                "Please provide something to search for",
                title="No search text",
                severity="error",
            )
            return
        guides = self._guides
        if not self.query_one("#global", Checkbox).value:
            if self._guide is None:
                self.notify(
                    "Unable to perform a non-global search when no guide is open",
                    title="Can't search",
                    severity="error",
                )
                return
            guides = [Guide(self._guide.title, self._guide.path)]
        self._search(
            guides,
            self.query_one(Input).value,
            self.query_one("#ignore_case", Checkbox).value,
        )

    @on(Button.Pressed, "#stop")
    def stop_search(self) -> None:
        """Stop the search."""
        self.app.workers.cancel_group(self, "search")


### search.py ends here
