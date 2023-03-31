from typing import Dict, Optional
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
import json
import pokebase
from models.pokemon_models import PokemonChanges, PokemonData
from models.move_models import MoveDetails

app = FastAPI()


origins = [
    "http://localhost",
    "http://localhost:5173",
    "http://localhost:5173/pokemon/*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/pokemon")
async def get_pokemon_list():
    with open(f"temp/pokemon.json", encoding="utf-8") as pokemon_file:
        pokemon = json.load(pokemon_file)
        pokemon_file.close()

    return list(pokemon.keys())


@app.get("/moves")
async def get_moves_list():
    with open(f"temp/moves.json", encoding="utf-8") as moves_file:
        moves = json.load(moves_file)
        moves_file.close()

    return list(moves.keys())


@app.get("/pokemon/{pokemon_name}")
async def get_pokemon(pokemon_name: str):
    with open(f"temp/pokemon.json", encoding="utf-8") as pokemon_file:
        pokemon = json.load(pokemon_file)
        pokemon_file.close()

    if pokemon_name not in pokemon:
        return {"message": "Pokemon not found", "status": 404}
    return pokemon[pokemon_name]


@app.post("/save-changes/pokemon/{pokemon_name}")
async def save_pokemon_changes(changes: PokemonChanges, pokemon_name: str):
    with open(f"temp/pokemon.json", encoding="utf-8") as pokemon_file:
        pokemon = json.load(pokemon_file)
        pokemon_file.close()

    if changes.types:
        pokemon[pokemon_name]["types"] = [
            type for type in changes.types if type != "None"
        ]

    if changes.abilities:
        pokemon[pokemon_name]["abilities"] = changes.abilities

    if changes.stats:
        for stat, value in changes.stats:
            pokemon[pokemon_name]["stats"][stat] = value

    if changes.evolution:
        pokemon[pokemon_name]["evolution"] = changes.evolution

    if changes.moves:
        for move, value in changes.moves.__root__.items():
            if value.delete:
                del pokemon[pokemon_name]["moves"][move]
                continue

            pokemon[pokemon_name]["moves"][move] = {
                "level_learned_at": value.level_learned_at,
                "learn_method": value.learn_method,
            }

    with open(f"temp/pokemon.json", "w") as pokemon_file:
        pokemon_file.write(json.dumps(pokemon))
        pokemon_file.close()

    with open(f"temp/updates/modified_pokemon.json", "r+") as changes_file:
        current_changes = json.load(changes_file)
        if pokemon_name not in current_changes["changed_pokemon"]:
            current_changes["changed_pokemon"].append(pokemon_name)
            changes_file.seek(0)
            changes_file.truncate()
            changes_file.write(json.dumps(current_changes))
        changes_file.close()

    return {"message": "Changes Saved"}


@app.get("/moves/{move_name}")
async def get_moves(move_name: str):
    with open(f"temp/moves.json", encoding="utf-8") as moves_file:
        moves = json.load(moves_file)
        moves_file.close()
    print(moves[move_name])

    return moves[move_name]


@app.post("/save-changes/moves/{move_name}")
def save_move_changes(move_details: MoveDetails, move_name: str):
    with open(f"temp/moves.json", encoding="utf-8") as moves_file:
        moves = json.load(moves_file)
        moves_file.close()

    if move_details.power:
        moves[move_name]["power"] = move_details.power

    if move_details.accuracy:
        moves[move_name]["accuracy"] = move_details.accuracy

    if move_details.pp:
        moves[move_name]["pp"] = move_details.pp

    if move_details.type:
        moves[move_name]["type"] = move_details.type

    if move_details.damage_class:
        moves[move_name]["damage_class"] = move_details.damage_class

    with open(f"temp/moves.json", "w") as moves_file:
        moves_file.write(json.dumps(moves))
        moves_file.close()

    with open(f"temp/updates/modified_moves.json", "r+") as moves_changes_file:
        current_changes = json.load(moves_changes_file)
        if move_name not in current_changes["changed_moves"]:
            current_changes["changed_moves"].append(move_name)
            moves_changes_file.seek(0)
            moves_changes_file.truncate()
            moves_changes_file.write(json.dumps(current_changes))
        moves_changes_file.close()

    return {"message": "Changes Saved"}
