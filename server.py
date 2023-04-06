from typing import Dict, Optional
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
import json
import pokebase
from models.pokemon_models import PokemonChanges, PokemonData
from models.move_models import MoveDetails
from routes import pokemon_routes, move_routes, matchups_routes

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


app.include_router(pokemon_routes.router)
app.include_router(move_routes.router)
app.include_router(matchups_routes.router)
