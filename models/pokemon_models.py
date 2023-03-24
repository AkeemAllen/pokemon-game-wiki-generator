from typing import Dict, Optional
from pydantic import BaseModel


class Stats(BaseModel):
    hp: Optional[int]
    attack: Optional[int]
    defense: Optional[int]
    sp_attack: Optional[int]
    sp_defense: Optional[int]
    speed: Optional[int]


class MoveData(BaseModel):
    level_learned_at: int
    learn_method: str
    delete: Optional[bool] = False


class Move(BaseModel):
    __root__: Dict[str, MoveData]


class Changes(BaseModel):
    id: Optional[int]
    types: Optional[list[str]]
    abilities: Optional[list[str]]
    stats: Optional[Stats]
    moves: Optional[Move]
    machine_moves: Optional[list[str]]
    evolution: Optional[str]


class PokemonChanges(BaseModel):
    __root__: Dict[str, Changes]


class PokemonData(BaseModel):
    id: int
    name: str
    types: list[str]
    abilities: list[str]
    stats: Stats
    moves: Move
    sprite: str
