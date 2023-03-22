from typing import Dict, Optional
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
import json
import pokebase
from models.pokemon_models import Changes, PokemonData


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


@app.get("/pokemon/{pokemon_name}")
async def get_pokemon(pokemon_name: str):
    with open(f"temp/pokemon.json", encoding="utf-8") as pokemon_file:
        pokemon = json.load(pokemon_file)
        pokemon_file.close()

    return pokemon[pokemon_name]


@app.post("/save-changes/{pokemon_name}")
async def save_pokemon_changes(changes: Changes, pokemon_name: str):
    with open(f"temp/pokemon.json", encoding="utf-8") as pokemon_file:
        pokemon = json.load(pokemon_file)
        pokemon_file.close()
    
    if changes.types:
        pokemon[pokemon_name]["types"] = changes.types
    if changes.abilities:
        pokemon[pokemon_name]["abilities"] = changes.abilities
    if changes.stats:
        pokemon[pokemon_name]["stats"] = changes.stats
   
    if not changes.moves or not changes.machine_moves:
        return {"message": "Changes Saved"}
    print("here") 
    with open(f"temp/moves.json", encoding='utf-8') as move_json_file:
        moves= json.load(move_json_file)
        move_json_file.close()
    
    if changes.moves:
        for move, value in changes.moves.__root__.items():
            pokemon[pokemon_name]["moves"][move] = {
                "id": moves[move]["id"],
                "level_learned_at": value,
                "learn_method": "level-up"
            }
   
    if changes.machine_moves:
        for move in changes.machine_moves:
            pokemon[pokemon_name]["moves"][move] = {
                "id": moves[move]["id"],
                "level_learned_at": 0,
                "learn_method": "machine"
            }
    
    with open(f"temp/pokemon.json", "w") as pokemon_file:
        pokemon_file.write(json.dumps(pokemon))
        pokemon_file.close()
 
    return {"message": "Changes Saved"}
