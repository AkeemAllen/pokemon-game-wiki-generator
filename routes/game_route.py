from fastapi import APIRouter
import json


router = APIRouter()


@router.get("/game_route")
async def get_game_route_list():
    with open(f"temp/routes.json", encoding="utf-8") as routes_file:
        routes = json.load(routes_file)
        routes_file.close()

    return list(routes.keys())


@router.get("/game_route/{route_name}")
async def get_game_route(route_name: str):
    with open(f"temp/routes.json", encoding="utf-8") as routes_file:
        routes = json.load(routes_file)
        routes_file.close()

    if route_name not in routes:
        return {"message": "Route not found", "status": 404}
    return routes[route_name]


# @router.post("/save-changes/game_route/{route_name}")
# async def save_route_changes()
