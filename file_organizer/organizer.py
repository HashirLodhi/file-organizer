"""Core file organization logic."""

import json
import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


# Default file type categories
DEFAULT_CATEGORIES: Dict[str, List[str]] = {
    "images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"],
    "documents": [".pdf", ".doc", ".docx", ".txt", ".md", ".rtf", ".odt"],
    "code": [".py", ".js", ".ts", ".java", ".c", ".cpp", ".go", ".rs"],
    "data": [".json", ".csv", ".xml", ".yaml", ".yml", ".toml"],
    "archives": [".zip", ".tar", ".gz", ".rar", ".7z"],
    "audio": [".mp3", ".wav", ".flac", ".aac", ".ogg"],
    "video": [".mp4", ".avi", ".mkv", ".mov", ".wmv"],
}

DEFAULT_IGNORE_PATTERNS = [
    ".git",
    "__pycache__",
    ".DS_Store",
    "Thumbs.db",
    "desktop.ini",
]


def should_ignore(filename: str, ignore_patterns: List[str] = None) -> bool:
    """
    Check if a file should be ignored based on patterns.

    Args:
        filename: Name of the file to check
        ignore_patterns: List of patterns to ignore

    Returns:
        True if the file should be ignored
    """
    if ignore_patterns is None:
        ignore_patterns = DEFAULT_IGNORE_PATTERNS

    for pattern in ignore_patterns:
        if filename == pattern or filename.endswith(f"/{pattern}"):
            return True
    return False


def get_category(filename: str, categories: Dict[str, List[str]] = None) -> str:
    """Determine the category for a file based on its extension."""
    if categories is None:
        categories = DEFAULT_CATEGORIES

    ext = Path(filename).suffix.lower()

    for category, extensions in categories.items():
        if ext in extensions:
            return category

    return "other"


def organize_files(
    source_dir: str,
    dry_run: bool = False,
    verbose: bool = False,
    categories: Dict[str, List[str]] = None,
    ignore_patterns: List[str] = None,
) -> Dict[str, List[str]]:
    """
    Organize files in the source directory by type.

    Args:
        source_dir: Path to the directory to organize
        dry_run: If True, only show what would be done
        verbose: If True, print detailed output
        categories: Custom category definitions

    Returns:
        Dictionary mapping categories to lists of moved files
    """
    source_path = Path(source_dir)

    if not source_path.exists():
        raise FileNotFoundError(f"Directory not found: {source_dir}")

    if not source_path.is_dir():
        raise NotADirectoryError(f"Not a directory: {source_dir}")

    moved_files: Dict[str, List[str]] = {}

    for item in source_path.iterdir():
        if item.is_file():
            if should_ignore(item.name, ignore_patterns):
                if verbose:
                    print(f"  {item.name} -> ignored")
                continue

            category = get_category(item.name, categories)
            dest_dir = source_path / category
            dest_path = dest_dir / item.name

            if verbose:
                print(f"  {item.name} -> {category}/")

            if not dry_run:
                dest_dir.mkdir(exist_ok=True)

                # Handle duplicate filenames
                counter = 1
                while dest_path.exists():
                    stem = item.stem
                    suffix = item.suffix
                    dest_path = dest_dir / f"{stem}_{counter}{suffix}"
                    counter += 1

                shutil.move(str(item), str(dest_path))

            if category not in moved_files:
                moved_files[category] = []
            moved_files[category].append(item.name)

    return moved_files


def generate_report(moved_files: Dict[str, List[str]], source_dir: str) -> str:
    """
    Generate a summary report of the organization.

    Args:
        moved_files: Dictionary mapping categories to file lists
        source_dir: The directory that was organized

    Returns:
        Formatted report string
    """
    total_files = sum(len(files) for files in moved_files.values())
    total_categories = len(moved_files)

    lines = [
        "=" * 50,
        "FILE ORGANIZATION REPORT",
        "=" * 50,
        f"Directory: {source_dir}",
        f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"Total files: {total_files}",
        f"Categories: {total_categories}",
        "-" * 50,
    ]

    for category in sorted(moved_files.keys()):
        files = moved_files[category]
        lines.append(f"\n{category}/ ({len(files)} files):")
        for f in sorted(files):
            lines.append(f"  - {f}")

    lines.append("=" * 50)
    return "\n".join(lines)


def save_report(moved_files: Dict[str, List[str]], source_dir: str, output_path: str = None) -> str:
    """
    Save organization report to a JSON file.

    Args:
        moved_files: Dictionary mapping categories to file lists
        source_dir: The directory that was organized
        output_path: Path to save the report (default: source_dir/report.json)

    Returns:
        Path to the saved report
    """
    if output_path is None:
        output_path = os.path.join(source_dir, "report.json")

    report = {
        "timestamp": datetime.now().isoformat(),
        "source_directory": source_dir,
        "total_files": sum(len(files) for files in moved_files.values()),
        "categories": {cat: files for cat, files in moved_files.items()},
    }

    with open(output_path, "w") as f:
        json.dump(report, f, indent=2)

    return output_path


def get_date_folder(filepath: Path, date_format: str = "year-month") -> str:
    """
    Get the folder name based on file modification date.

    Args:
        filepath: Path to the file
        date_format: Format for date folder ('year', 'year-month', or 'full')

    Returns:
        Folder name string
    """
    mtime = datetime.fromtimestamp(filepath.stat().st_mtime)

    if date_format == "year":
        return str(mtime.year)
    elif date_format == "year-month":
        return f"{mtime.year}/{mtime.month:02d}"
    else:
        return f"{mtime.year}/{mtime.month:02d}/{mtime.day:02d}"


def organize_by_date(
    source_dir: str,
    dry_run: bool = False,
    verbose: bool = False,
    date_format: str = "year-month",
) -> Dict[str, List[str]]:
    """
    Organize files in the source directory by modification date.

    Args:
        source_dir: Path to the directory to organize
        dry_run: If True, only show what would be done
        verbose: If True, print detailed output
        date_format: Format for date folders ('year', 'year-month', or 'full')

    Returns:
        Dictionary mapping date folders to lists of moved files
    """
    source_path = Path(source_dir)

    if not source_path.exists():
        raise FileNotFoundError(f"Directory not found: {source_dir}")

    if not source_path.is_dir():
        raise NotADirectoryError(f"Not a directory: {source_dir}")

    moved_files: Dict[str, List[str]] = {}

    for item in source_path.iterdir():
        if item.is_file():
            date_folder = get_date_folder(item, date_format)
            dest_dir = source_path / date_folder
            dest_path = dest_dir / item.name

            if verbose:
                print(f"  {item.name} -> {date_folder}/")

            if not dry_run:
                dest_dir.mkdir(parents=True, exist_ok=True)

                counter = 1
                while dest_path.exists():
                    stem = item.stem
                    suffix = item.suffix
                    dest_path = dest_dir / f"{stem}_{counter}{suffix}"
                    counter += 1

                shutil.move(str(item), str(dest_path))

            if date_folder not in moved_files:
                moved_files[date_folder] = []
            moved_files[date_folder].append(item.name)

    return moved_files
