from enum import Enum
from typing import Dict, Optional
from pydantic import BaseModel


class Stats(BaseModel):
    hp: Optional[int]
    attack: Optional[int]
    defense: Optional[int]
    sp_attack: Optional[int]
    sp_defense: Optional[int]
    speed: Optional[int]


class MoveDetails(BaseModel):
    power: Optional[int]
    accuracy: Optional[int]
    pp: Optional[int]
    type: Optional[str]
    damage_class: Optional[str]


class MoveData(BaseModel):
    level_learned_at: int
    learn_method: str
    delete: Optional[bool] = False


class Move(BaseModel):
    __root__: Dict[str, MoveData]


class PokemonChanges(BaseModel):
    id: Optional[int]
    types: Optional[list[str]]
    abilities: Optional[list[str]]
    stats: Optional[Stats]
    moves: Optional[Move]
    machine_moves: Optional[list[str]]
    evolution: Optional[str]


class PokemonData(BaseModel):
    id: Optional[int]
    name: Optional[str]
    types:Optional[list[str]]
    abilities: Optional[list[str]]
    stats: Optional[Stats]
    moves: Optional[Move]
    sprite: Optional[str]
    evolution: Optional[str]

class PokemonVersions (Enum):
    RED_BLUE = "red-blue"
    YELLOW = "yellow"
    GOLD_SILVER = "gold-silver"
    CRYSTAL = "crystal"
    RUBY_SAPPHIRE = "ruby-sapphire"
    EMERALD = "emerald"
    FIRERED_LEAFGREEN = "firered-leafgreen"
    DIAMOND_PEARL = "diamond-pearl"
    PLATINUM = "platinum"
    HEARTGOLD_SOULSILVER = "heartgold-soulsilver"
    BLACK_WHITE = "black-white"
    BLACKTWO_WHITETWO = "black-2-white-2"
    X_Y = "x-y"
    OMEGARUBY_ALPHASAPPHIRE = "omega-ruby-alpha-sapphire"
    SUN_MOON = "sun-moon"
    ULTRASUN_ULTRAMOON = "ultra-sun-ultra-moon"
    SWORD_SHEILD = "sword-shield"


pokemon_versions_ordered = {
    PokemonVersions.RED_BLUE: 0,
    PokemonVersions.YELLOW: 1,
    PokemonVersions.GOLD_SILVER: 2,
    PokemonVersions.CRYSTAL: 3,
    PokemonVersions.RUBY_SAPPHIRE: 4,
    PokemonVersions.EMERALD: 5,
    PokemonVersions.FIRERED_LEAFGREEN: 6,
    PokemonVersions.DIAMOND_PEARL: 7,
    PokemonVersions.BLACK_WHITE: 8,
    PokemonVersions.BLACKTWO_WHITETWO: 9,
    PokemonVersions.X_Y: 10,
    PokemonVersions.OMEGARUBY_ALPHASAPPHIRE: 11,
    PokemonVersions.SUN_MOON: 12,
    PokemonVersions.ULTRASUN_ULTRAMOON: 13,
    PokemonVersions.SWORD_SHEILD: 14
}