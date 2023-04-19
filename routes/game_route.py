from fastapi import APIRouter
import json

from models.game_route_models import RouteProperties


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


@router.post("/game_route/{route_name}")
async def create_game_route(route_name: str, route_properties: RouteProperties):
    with open(f"temp/routes.json", encoding="utf-8") as routes_file:
        routes = json.load(routes_file)
        routes_file.close()

    if route_name in routes:
        return {"message": "Route already exists", "status": 400}

    routes[route_name] = {}

    routes[route_name] = route_properties.dict(exclude_none=True)

    with open(f"temp/routes.json", "w", encoding="utf-8") as routes_file:
        routes_file.write(json.dumps(routes))
        routes_file.close()

    return {"message": "Route created", "status": 200}


@router.post("/save-changes/game_route/{route_name}")
async def save_route_changes(route_name: str, route_properties: RouteProperties):
    with open(f"temp/routes.json", encoding="utf-8") as routes_file:
        routes = json.load(routes_file)
        routes_file.close()

    if route_name not in routes:
        return {"message": "Route not found", "status": 404}

    routes[route_name] = route_properties.dict(exclude_none=True)

    with open(f"temp/routes.json", "w", encoding="utf-8") as routes_file:
        routes_file.write(json.dumps(routes))
        routes_file.close()

    return {"message": "Route changes saved", "status": 200}
