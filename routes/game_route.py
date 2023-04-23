from fastapi import APIRouter
import json

from models.game_route_models import Route, RouteProperties


router = APIRouter()


@router.get("/game_routes")
async def get_game_route_list():
    with open(f"temp/routes.json", encoding="utf-8") as routes_file:
        routes = json.load(routes_file)
        routes_file.close()

    return routes


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
async def save_single_route_changes(route_name: str, route_properties: RouteProperties):
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


@router.post("/save-changes/game_routes")
async def save_route_changes(routes: Route):
    with open(f"temp/routes.json", "w") as routes_file:
        routes_file.write(routes.json(exclude_none=True))
        routes_file.close()

    return {"message": "Route changes saved", "status": 200}
