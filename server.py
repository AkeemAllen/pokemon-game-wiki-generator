from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import matchups, move, pokemon, game_route, items, natures, abilities

app = FastAPI()


origins = [
    "*",
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
app.include_router(items.router)
app.include_router(natures.router)
app.include_router(abilities.router)
