from pathlib import Path
import yaml

_CFG_PATH = Path(__file__).resolve().parents[2] / "config.yaml"  

if not _CFG_PATH.is_file():
    raise FileNotFoundError(
        "config.yaml not found in the current directory. "
        "Please run from the repo root and ensure a config.yaml exists."
    )

with _CFG_PATH.open("r") as f:
    _cfg = yaml.safe_load(f) or {}

def _req(key: str) -> str:
    v = _cfg.get(key)
    if not v:
        raise RuntimeError(f"Missing required config key: {key}")
    return v

class Config:
    # Admin API base URL (used by the client to call the server)
    BASE_URL   = _req("base_url")

    # (Optional) If your client ever needs these later, keep them here
    # MONGO_URI  = _cfg.get("mongo_uri", "")
    # RULES_DB   = _cfg.get("rules_db", "")
    # TAPIS_URL  = _cfg.get("tapis_url", "")
    # TAPIS_USER = _cfg.get("tapis_user", "")
    # TAPIS_PASS = _cfg.get("tapis_pass", "")