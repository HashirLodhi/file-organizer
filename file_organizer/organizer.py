"""Core file organization logic."""

import os
import shutil
from pathlib import Path
from typing import Dict, List


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
