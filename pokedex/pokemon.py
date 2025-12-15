from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass(frozen=True)
class Pokemon:
    """Data model for a Pokémon."""
    id: int
    name: str
    types: List[str]
    stats: Dict[str, int]
    height: Optional[int] = None   # decimeters
    weight: Optional[int] = None   # hectograms
    sprite_url: Optional[str] = None

    @classmethod
    def from_pokeapi(cls, data: dict) -> "Pokemon":
        pid = int(data["id"])
        name = str(data.get("name", "")).title()

        types = sorted(
            t["type"]["name"].title()
            for t in data.get("types", [])
        )

        stats = {
            s["stat"]["name"]: int(s["base_stat"])
            for s in data.get("stats", [])
        }

        sprites = data.get("sprites") or {}
        sprite_url = sprites.get("front_default")

        return cls(
            id=pid,
            name=name,
            types=types,
            stats=stats,
            height=data.get("height"),
            weight=data.get("weight"),
            sprite_url=sprite_url,
        )

    def height_weight_str(self) -> str:
        """Return height and weight in human-readable units."""
        if self.height is None or self.weight is None:
            return "Height/Weight: Unknown"

        height_m = self.height / 10      # dm → meters
        weight_kg = self.weight / 10     # hg → kg
        return f"Height: {height_m:.1f} m | Weight: {weight_kg:.1f} kg"

    def short_summary(self) -> str:
        types_str = "/".join(self.types) if self.types else "Unknown"
        hp = self.stats.get("hp", "?")
        atk = self.stats.get("attack", "?")
        defense = self.stats.get("defense", "?")
        return (
            f"#{self.id} {self.name} ({types_str}) | "
            f"HP {hp} ATK {atk} DEF {defense}"
        )

