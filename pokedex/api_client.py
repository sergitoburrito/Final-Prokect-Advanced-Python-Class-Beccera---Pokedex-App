from __future__ import annotations
import requests
from typing import Optional

from storage import load_cached_json, save_cached_json


class PokeAPIClient:
    BASE = "https://pokeapi.co/api/v2"

    def get_pokemon_raw(self, name_or_id: str, *, use_cache: bool = True) -> Optional[dict]:
        key = name_or_id.strip().lower()
        if not key:
            return None

        if use_cache:
            cached = load_cached_json(key)
            if cached:
                return cached

        url = f"{self.BASE}/pokemon/{key}"
        try:
            resp = requests.get(url, timeout=10)
            if resp.status_code != 200:
                return None
            data = resp.json()
        except requests.RequestException:
            return None

        
        try:
            save_cached_json(key, data)
            if "id" in data:
                save_cached_json(str(data["id"]), data)
            if "name" in data:
                save_cached_json(str(data["name"]), data)
        except Exception:
            pass

        return data

