from __future__ import annotations

from importlib import resources
from pathlib import Path
from typing import Any, Dict

import yaml

_CWD_OVERRIDE = Path("config.yaml")

def _load_yaml(p: Path) -> Dict[str, Any]:
    with p.open("r") as f:
        return yaml.safe_load(f) or {}

def _load_config() -> Dict[str, Any]:
    if _CWD_OVERRIDE.is_file():
        return _load_yaml(_CWD_OVERRIDE)

    with resources.files("database.rules_engine").joinpath("config.yaml").open("r") as f:
        return yaml.safe_load(f) or {}

_cfg = _load_config()

def _req(key: str) -> str:
    v = _cfg.get(key)
    if not v:
        raise RuntimeError(f"Missing required config key: {key}")
    return v

class Config:
    # Admin API base URL used by the client
    BASE_URL = _req("base_url")