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
        pokemon[pokemon_name]["types"] = [type for type in changes.types if type != "None"]
    if changes.abilities:
        pokemon[pokemon_name]["abilities"] = changes.abilities
    if changes.stats:
        for stat, value in changes.stats:
            pokemon[pokemon_name]["stats"][stat] = value

    with open(f"temp/moves.json", encoding='utf-8') as move_json_file:
        moves = json.load(move_json_file)
        move_json_file.close()
    
    if changes.moves:
        print(pokemon[pokemon_name]["moves"])
        # pokemon[pokemon_name]["moves"] = json.load(changes.moves.json())
        for move, value in changes.moves.__root__.items():
            if value.delete:
                del pokemon[pokemon_name]["moves"][move]
                continue
            
            pokemon[pokemon_name]["moves"][move] = {
                "level_learned_at": value.level_learned_at,
                "learn_method": value.learn_method
            }
     
    with open(f"temp/pokemon.json", "w") as pokemon_file:
        pokemon_file.write(json.dumps(pokemon))
        pokemon_file.close()
    
    with open(f"updates/modified_pokemon.json", "r+") as changes_file:
        current_changes = json.load(changes_file)
        if pokemon_name not in current_changes["changed_pokemon"]:
            current_changes["changed_pokemon"].append(pokemon_name)
            changes_file.seek(0)
            changes_file.truncate()
            changes_file.write(json.dumps(current_changes))
        changes_file.close()
 
    return {"message": "Changes Saved"}
