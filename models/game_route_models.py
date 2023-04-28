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

    # This is here just to capture
    # the level ranage of wild pokemon since it can
    # be different for each area on the route
    area_level: Optional[str]


class Encounters(BaseModel):
    __root__: Dict[str, list[TrainerOrWildPokemon]]


class Trainers(BaseModel):
    __root__: Dict[str, list[TrainerOrWildPokemon]]


class AreaLevels(BaseModel):
    __root__: Dict[str, str]


class RouteProperties(BaseModel):
    position: int
    wild_encounters: Optional[Encounters]
    trainers: Optional[Trainers]
    important_trainers: Optional[Trainers]
    wild_encounters_area_levels: Optional[AreaLevels]


class NewRouteName(BaseModel):
    new_route_name: str


class Route(BaseModel):
    __root__: Dict[str, RouteProperties]
