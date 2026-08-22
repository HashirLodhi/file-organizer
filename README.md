# File Organizer CLI

A simple Python CLI tool to organize files by type, date, or custom rules.

## Installation

```bash
pip install -e .
```

## Usage

```bash
# Organize files by type (images, documents, code, etc.)
file-organize ~/Downloads

# Dry run mode (preview changes without moving files)
file-organize ~/Downloads --dry-run

# Verbose output
file-organize ~/Downloads --verbose
```

## Features

- Organize files by extension type
- Dry run mode to preview changes
- Verbose logging
- Safe file handling (no overwrites)

## Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/
```

## License

MIT
