# AgiNG - A Norton Guide reader for the terminal

![AgiNG](https://raw.githubusercontent.com/davep/aging/refs/heads/main/.images/aging-social-banner.png)

## Introduction

AgiNG is the latest in [a long line of Norton Guide tools and
readers](https://www.davep.org/norton-guides/) I've written, starting in the
1990s. It is designed to be as comprehensive as possible, keyboard-first but
mouse-friendly, and to look as good as possible.

## Installing

### pipx

The application can be installed using [`pipx`](https://pypa.github.io/pipx/):

```sh
$ pipx install aging
```

Once installed run the `aging` command.

### Homebrew

The package is available via Homebrew. Use the following commands to install:

```sh
$ brew tap davep/homebrew
$ brew install aging
```

Once installed run the `aging` command.

## Using AgiNG

The best way to get to know AgiNG is to read the help screen. Once in the
application you can see this by pressing <kbd>F1</kbd>.

![AgiNG Help](https://raw.githubusercontent.com/davep/aging/refs/heads/main/.images/aging-help-screen.png)

Commands can also be discovered via the command palette
(<kbd>ctrl</kbd>+<kbd>p</kbd>):

![The command palette](https://raw.githubusercontent.com/davep/aging/refs/heads/main/.images/aging-command-palette.png)

## Features

- Manage a directory of all of your Norton Guide files.
- Read Norton Guide files (obviously!).
- Clipboard support (copy text or copy source).
- A command palette to make it easy to discover commands and their keys.
- A rich help screen to make it easy to discover commands and their keys.
- [More as time goes on](https://github.com/davep/aging/issues?q=is%3Aissue+is%3Aopen+label%3ATODO).

## File locations

AgiNG stores files in a `aging` directory within both [`$XDG_DATA_HOME` and
`$XDG_CONFIG_HOME`](https://specifications.freedesktop.org/basedir-spec/latest/).
If you wish to fully remove anything to do with AgiNG you will need to
remove those directories too.

Expanding for the common locations, the files normally created are:

- `~/.config/aging/configuration.json` -- The configuration file.
- `~/.local/share/aging/*.json` -- The locally-held data.

## Getting help

If you need help, or have any ideas, please feel free to [raise an
issue](https://github.com/davep/aging/issues) or [start a
discussion](https://github.com/davep/aging/discussions).

## TODO

See [the TODO tag in
issues](https://github.com/davep/aging/issues?q=is%3Aissue+is%3Aopen+label%3ATODO)
to see what I'm planning.

[//]: # (README.md ends here)
