# PentUI

> A keyboard-first, YAML-driven Nmap terminal interface built with Python and Textual.

PentUI is an early MVP focused on Nmap. Its configuration is stored in
[`tools/nmap.yaml`](tools/nmap.yaml), so future tool integrations can reuse the
same interface and command-building architecture.

## Features

- Full-screen Nmap configuration—not a permanent split pane.
- Reactive, safe command preview built from an argument list rather than a shell command.
- 111 documented Nmap flags organized into clear groups.
- Input modal for flags that need values, plus target validation.
- Asynchronous execution with live output and a mid-scan stop control.
- Configuration remains available when returning to the tool selection screen.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

After the launcher is installed, simply run `pentui` from any directory. It uses
the project's `.venv` automatically (and creates it with the required packages
if it is missing).

Nmap itself must be installed separately and available on `PATH`. PentUI detects it at startup and will not execute a scan if it is unavailable.

> Only scan systems and networks you own or have explicit permission to assess.

## Controls

- Arrow keys: move focus
- Space / Enter: select a flag, or edit an option that needs a value
- `R`: validate and run the current Nmap configuration
- `Esc`: return to the previous screen
- `Q`: quit (on the output screen it stops output streaming)

The execution screen also has a visible **Stop scan** button. It cancels the
running process and returns to the Nmap configuration screen, keeping the
current selections and target in place.

Enter a target in the dedicated target field. The command preview updates immediately for flags, parameter values, and target edits.

## Project layout

```text
pentui/             Application package
  core/             Definitions, command building, validation, execution
  tui/              Textual screens and styles
tools/nmap.yaml     Nmap flag catalog and descriptions
tests/              Automated tests
bin/pentui          Virtual-environment-aware launcher
```

## Test

```bash
python -m pytest
```

## Architecture

- `pentui/core/` contains definition models, YAML loading, safe argv construction, validation, and async process execution.
- `pentui/tui/` contains Textual screens and widgets only; Nmap option details never live in the UI code.
- `tools/nmap.yaml` declares metadata, groups, flags, value types, choices, and placeholders.
- `tests/` verifies command building, validation, and YAML loading.

Commands are executed as an argument list with `asyncio.create_subprocess_exec`, never through a shell string.

## Contributing

Contributions are welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md) before
opening a pull request. For security-sensitive reports, see [SECURITY.md](SECURITY.md).

## Status

This is an MVP. Nmap is the only implemented tool; the architecture is designed
to support future YAML-defined tools without rewriting the UI.
