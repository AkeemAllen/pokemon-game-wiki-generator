from typing import Dict, Optional, Union
from pydantic import BaseModel


class TrainerOrWildPokemon(BaseModel):
    name: Optional[str]
    level: Optional[int]
    moves: Optional[list[str]]
    item: Optional[str]
    nature: Optional[str]
    ability: Optional[str]
    catch_rate: Optional[int]

    # This is here just to capture
    # the level ranage of wild pokemon since it can
    # be different for each area on the route
    area_level: Optional[str]


class Encounters(BaseModel):
    __root__: Dict[str, list[TrainerOrWildPokemon]]


class Trainers(BaseModel):
    __root__: Dict[str, list[TrainerOrWildPokemon]]


class RouteProperties(BaseModel):
    wild_encounters: Optional[Encounters]
    trainers: Optional[Trainers]
    important_trainers: Optional[Trainers]


class Route(BaseModel):
    __root__: Dict[str, RouteProperties]
