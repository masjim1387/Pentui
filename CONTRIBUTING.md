# Contributing to PentUI

Thanks for contributing.

## Development setup

```bash
git clone https://github.com/masjim1387/PentUI.git
cd PentUI
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m pytest
```

## Pull requests

- Keep each pull request focused on one change.
- Add or update tests for core-logic changes.
- Run `python -m pytest` before opening the pull request.
- Keep tool-specific metadata in `tools/*.yaml`; avoid embedding it in UI widgets.
- Do not add functionality intended to scan systems without authorization.

## Commit messages

Use concise, imperative messages, for example: `Add XML output validation`.
