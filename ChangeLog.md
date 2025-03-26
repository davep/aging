# AgiNG ChangeLog

## v0.4.0

**Released: 2025-03-26**

- When doing a guide-wide search in the global search dialog, only the entry
  progress is now shown; the guides progress is now only visible when doing
  an all-guides search. ([#33](https://github.com/davep/aging/pull/33))

## v0.3.0

**Released: 2025-03-22**

- Added the ability to search for text within the current entry.
  ([#18](https://github.com/davep/aging/pull/18))
- Added the ability to search for text within all entries of the current
  guide. ([#18](https://github.com/davep/aging/pull/18))
- Added the ability to search for text within all entries of all guides
  added to the guide directory.
  ([#18](https://github.com/davep/aging/pull/18))
- Improved handling of corrupted/truncated guides, ensuring the app shows an
  error to the user rather than crashing.
  ([#23](https://github.com/davep/aging/pull/23))
- Fully hide the menu pane if we encounter a guide that has zero menus.
  ([#24](https://github.com/davep/aging/pull/24))

## v0.2.0

**Released: 2025-03-14**

- Fixed not being able to navigate into a child entry by mouse-clicking on a
  highlighted line. ([#11](https://github.com/davep/aging/pull/11))
- Added the ability to rename the title of a guide as it appears in the
  guide directory. ([#13](https://github.com/davep/aging/pull/13))
- Added the ability to remove a guide from the guide directory.
  ([#13](https://github.com/davep/aging/pull/13))
- Added the ability to remove all guides from the guide directory.
  ([#13](https://github.com/davep/aging/pull/13))
- The dialog for adding guides to the guide directory now remembers the
  last-selected directory, and starts from there on next use.
  (#14[](https://github.com/davep/aging/pull/14))
- When browsing to open an individual guide from the filesystem the
  application remembers the last location a guide was opened from and starts
  there. (#14[](https://github.com/davep/aging/pull/14))

## v0.1.0

**Released: 2025-03-11**

- Initial release.

## v0.0.1

**Released: 2025-02-28**

- Initial placeholder package to test that the name is available in PyPI.

[//]: # (ChangeLog.md ends here)
