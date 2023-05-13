from typing import Dict, Optional, Union
from pydantic import BaseModel


class TrainerOrWildPokemon(BaseModel):
    id: Optional[int]
    name: Optional[str]
    level: Optional[int]
    moves: Optional[list[str]]
    item: Optional[str]
    nature: Optional[str]
    ability: Optional[str]
    encounter_rate: Optional[int]


class Encounters(BaseModel):
    __root__: Dict[str, list[TrainerOrWildPokemon]]


class TrainerInfo(BaseModel):
    is_important: bool
    pokemon: list[TrainerOrWildPokemon]
    sprite_url: Optional[str]


class Trainers(BaseModel):
    __root__: Dict[str, TrainerInfo]


class AreaLevels(BaseModel):
    __root__: Dict[str, str]


class RouteProperties(BaseModel):
    position: int
    wild_encounters: Optional[Encounters]
    trainers: Optional[Trainers]
    wild_encounters_area_levels: Optional[AreaLevels]


class Route(BaseModel):
    __root__: Dict[str, RouteProperties]


class NewRoute(BaseModel):
    current_route_name: Optional[str]
    new_route_name: str
