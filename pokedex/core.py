from __future__ import annotations
from typing import Optional

from api_client import PokeAPIClient
from pokemon import Pokemon
from storage import load_favorites, save_favorites


class PokedexCore:
    """App logic (no GUI): search + favorites."""
    def __init__(self) -> None:
        self.api = PokeAPIClient()
        self.favorites: list[str] = load_favorites()

    def search(self, name_or_id: str) -> Optional[Pokemon]:
        raw = self.api.get_pokemon_raw(name_or_id)
        if not raw:
            return None
        return Pokemon.from_pokeapi(raw)

    def add_favorite(self, pokemon_name: str) -> None:
        name = pokemon_name.strip().title()
        if name and name not in self.favorites:
            self.favorites.append(name)
            save_favorites(self.favorites)

    def remove_favorite(self, pokemon_name: str) -> None:
        name = pokemon_name.strip().title()
        if name in self.favorites:
            self.favorites.remove(name)
            save_favorites(self.favorites)
    def list_favorites(self) -> list[str]:
        return list(self.favorites)

    def is_favorite(self, pokemon_name: str) -> bool:
        return pokemon_name.strip().title() in self.favorites
