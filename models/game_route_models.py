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

    # the feature below this is shelved for now
    # Rivals can have different teams depending on certain factors,
    # such as the chosen starter chosen. rival_version lists which version
    # of the rival's team this pokemon is on
    trainer_version: Optional[list[str]]


class Encounters(BaseModel):
    __root__: Dict[str, list[TrainerOrWildPokemon]]


class TrainerInfo(BaseModel):
    is_important: bool
    pokemon: list[TrainerOrWildPokemon]
    sprite_name: Optional[str]

    # the features below this are shelved for now
    # has_diff_versions: Optional[bool]
    trainer_versions: Optional[list[str]]


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
