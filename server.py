from typing import Dict, Optional
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
import json
import pokebase
from models.pokemon_models import PokemonChanges, PokemonData
from models.move_models import MoveDetails
from routes import matchups, move, pokemon, game_route

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


app.include_router(pokemon.router)
app.include_router(move.router)
app.include_router(matchups.router)
app.include_router(game_route.router)
