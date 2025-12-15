import json
from pathlib import Path
from typing import Optional

CACHE_DIR = Path("cache")
FAVORITES_FILE = Path("favorites.json")


def ensure_dirs() -> None:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)


def _safe_key(key: str) -> str:
    return key.strip().lower().replace(" ", "_")


def cache_path(key: str) -> Path:
    return CACHE_DIR / f"{_safe_key(key)}.json"


def load_cached_json(key: str) -> Optional[dict]:
    path = cache_path(key)
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def save_cached_json(key: str, data: dict) -> None:
    ensure_dirs()
    path = cache_path(key)
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def load_favorites() -> list[str]:
    if not FAVORITES_FILE.exists():
        return []
    try:
        data = json.loads(FAVORITES_FILE.read_text(encoding="utf-8"))
        if isinstance(data, list):
            return [str(x) for x in data]
    except Exception:
        pass
    return []


def save_favorites(favs: list[str]) -> None:
    
    clean = sorted(set(x.strip().title() for x in favs if str(x).strip()))
    FAVORITES_FILE.write_text(json.dumps(clean, indent=2), encoding="utf-8")
