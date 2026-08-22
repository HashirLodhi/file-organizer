"""Tests for file organizer."""

import os
import tempfile
from pathlib import Path

import pytest

from file_organizer.organizer import get_category, organize_files


def test_get_category_images():
    """Test image file categorization."""
    assert get_category("photo.jpg") == "images"
    assert get_category("icon.png") == "images"
    assert get_category("banner.svg") == "images"


def test_get_category_documents():
    """Test document file categorization."""
    assert get_category("report.pdf") == "documents"
    assert get_category("notes.txt") == "documents"
    assert get_category("readme.md") == "documents"


def test_get_category_code():
    """Test code file categorization."""
    assert get_category("main.py") == "code"
    assert get_category("index.js") == "code"
    assert get_category("app.ts") == "code"


def test_get_category_other():
    """Test unknown file categorization."""
    assert get_category("unknown.xyz") == "other"
    assert get_category("noextension") == "other"


def test_organize_files_dry_run():
    """Test dry run mode doesn't move files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create test files
        (Path(tmpdir) / "test.jpg").touch()
        (Path(tmpdir) / "doc.pdf").touch()
        (Path(tmpdir) / "script.py").touch()

        result = organize_files(tmpdir, dry_run=True)

        # Files should not be moved
        assert (Path(tmpdir) / "test.jpg").exists()
        assert (Path(tmpdir) / "doc.pdf").exists()
        assert (Path(tmpdir) / "script.py").exists()

        # But result should show what would be moved
        assert "images" in result
        assert "documents" in result
        assert "code" in result


def test_organize_files_real():
    """Test actual file organization."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create test files
        (Path(tmpdir) / "photo.jpg").touch()
        (Path(tmpdir) / "report.pdf").touch()

        result = organize_files(tmpdir, dry_run=False)

        # Files should be moved
        assert not (Path(tmpdir) / "photo.jpg").exists()
        assert not (Path(tmpdir) / "report.pdf").exists()

        assert (Path(tmpdir) / "images" / "photo.jpg").exists()
        assert (Path(tmpdir) / "documents" / "report.pdf").exists()
