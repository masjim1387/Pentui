# PentUI

PentUI is a small, keyboard-first Textual launcher for security tools. This MVP implements only Nmap and keeps the tool configuration in `tools/nmap.yaml` so later tools can use the same UI/core architecture.

## Install and run

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
