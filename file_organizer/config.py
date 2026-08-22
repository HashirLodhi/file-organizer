"""Configuration handling for file organizer."""

from pathlib import Path
from typing import Dict, List, Optional

import yaml


DEFAULT_CONFIG_PATH = Path.home() / ".config" / "file-organizer" / "config.yaml"


def load_config(config_path: Optional[str] = None) -> Dict:
    """Load configuration from a YAML file."""
    path = Path(config_path) if config_path else DEFAULT_CONFIG_PATH

    if not path.exists():
        return {}

    with open(path, "r") as f:
        return yaml.safe_load(f) or {}


def get_categories(config: Dict) -> Optional[Dict[str, List[str]]]:
    """Extract categories from config, or return None for defaults."""
    return config.get("categories")
