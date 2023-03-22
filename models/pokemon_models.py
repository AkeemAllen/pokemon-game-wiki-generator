from typing import Dict, Optional
from pydantic import BaseModel


class Stats(BaseModel):
    hp: Optional[float]
    attack: Optional[float]
    defense: Optional[float]
    sp_attack: Optional[float]
    sp_defense: Optional[float]
    speed: Optional[float]


class MoveData(BaseModel):
    id: int
    level_learned_at: int
    learn_method: str


class Move(BaseModel):
    __root__: Dict[str, MoveData]

class ChangeMove(BaseModel):
    __root__: Dict[str, int]

class Changes(BaseModel):
    id: int
    types: Optional[list[str]]
    abilities: Optional[list[str]]
    stats: Optional[Stats]
    moves: Optional[ChangeMove]
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
