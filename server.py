from typing import Dict, Optional
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import json
from pydantic import BaseModel
import pokebase

app = FastAPI()


origins = [
    "http://localhost",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Stats(BaseModel):
    hp: Optional[float]
    attack: Optional[float]
    defense: Optional[float]
    special_attack: Optional[float]
    special_defense: Optional[float]
    speed: Optional[float]


class Move(BaseModel):
    __root__: Dict[str, int]


class Changes(BaseModel):
    id: int
    types: Optional[list[str]]
    abilities: Optional[list[str]]
    stats: Optional[Stats]
    moves: Optional[Move]
    machine_moves: Optional[list[str]]
    evolution: Optional[str]


class Pokemon(BaseModel):
    __root__: Dict[str, Changes]


@app.get("/pokemon/{pokemon_name}")
async def get_pokemon(pokemon_name: str):
    dex_number = pokebase.pokemon(pokemon_name).id
    with open(f"temp/pokemon/{dex_number}.json", encoding="utf-8") as pokemon_file:
        pokemon_data = json.load(pokemon_file)
        pokemon_file.close()

    return pokemon_data


@app.post("/generate")
async def generate_pokemon_changes_file(changes: Pokemon):
    print(changes.json(exclude_none=True))
    with open("updates/test/changes.json", "w") as pokemon_changes_file:
        pokemon_changes_file.write(changes.json(exclude_none=True))
        pokemon_changes_file.close()
 
    return {"message": "Changes Saved"}


@app.get("/")
async def test():
    return {"message": "Changes Saved"}
