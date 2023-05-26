from typing import Optional
from fastapi import APIRouter
import json

from models.game_route_models import NewRoute, RouteProperties
from utils import get_sorted_routes


router = APIRouter()


# Get all routes and return them as sorted dict
@router.get("/game-routes")
async def get_game_route_list():
    with open(f"temp/routes.json", encoding="utf-8") as routes_file:
        routes = json.load(routes_file)
        routes_file.close()

    return get_sorted_routes(routes)


# Get route by name
@router.get("/game-route/{route_name}")
async def get_game_route(route_name: str):
    with open(f"temp/routes.json", encoding="utf-8") as routes_file:
        routes = json.load(routes_file)
        routes_file.close()

    if route_name not in routes:
        return {"message": "Route not found", "status": 404}
    return routes[route_name]


@router.post("/game-route")
async def create_game_route(new_route: NewRoute):
    with open(f"temp/routes.json", encoding="utf-8") as routes_file:
        routes = json.load(routes_file)
        routes_file.close()

    if new_route.new_route_name in routes:
        return {"message": "Route already exists", "status": 400}

    routes[new_route.new_route_name] = {"position": len(routes) + 1}

    with open(f"temp/routes.json", "w", encoding="utf-8") as routes_file:
        routes_file.write(json.dumps(routes))
        routes_file.close()

    return {
        "message": "Route created",
        "status": 200,
        "routes": get_sorted_routes(routes),
    }


# Edit route name
@router.post("/game-route/edit-route-name/")
async def edit_game_route(new_route: NewRoute):
    with open(f"temp/routes.json", encoding="utf-8") as routes_file:
        routes = json.load(routes_file)
        routes_file.close()

    if routes[new_route.current_route_name] is None:
        return {"message": "Route not found", "status": 404}

    routes[new_route.new_route_name] = routes[new_route.current_route_name]

    del routes[new_route.current_route_name]

    with open(f"temp/routes.json", "w", encoding="utf-8") as routes_file:
        routes_file.write(json.dumps(routes))
        routes_file.close()

    return {
        "message": "Route edited",
        "status": 200,
        "routes": get_sorted_routes(routes),
    }


# Save changes to route
@router.patch("/game-route/edit/{route_name}")
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

    return {
        "message": "Route changes saved",
        "status": 200,
        "routes": get_sorted_routes(routes),
    }


# Delete route by name
@router.delete("/game-route/delete/{route_name}")
async def delete_route(route_name: str):
    with open(f"temp/routes.json", encoding="utf-8") as routes_file:
        routes = json.load(routes_file)
        routes_file.close()

    if route_name not in routes:
        return {"message": "Route not found", "status": 404}

    del routes[route_name]

    with open(f"temp/routes.json", "w", encoding="utf-8") as routes_file:
        routes_file.write(json.dumps(routes))
        routes_file.close()

    return {
        "message": "Route deleted",
        "status": 200,
        "routes": get_sorted_routes(routes),
    }


@router.post("/game-route/duplicate/{route_name}/{new_route_name}")
async def duplicate_route(route_name: str, new_route_name: str):
    with open(f"temp/routes.json", encoding="utf-8") as routes_file:
        routes = json.load(routes_file)
        routes_file.close()

    if route_name not in routes:
        return {"message": "Route not found", "status": 404}

    routes[new_route_name] = {
        **routes[route_name],
    }
    routes[new_route_name]["position"] = len(routes)

    with open(f"temp/routes.json", "w", encoding="utf-8") as routes_file:
        routes_file.write(json.dumps(routes))
        routes_file.close()

    return {
        "message": "Route duplicated",
        "status": 200,
        "routes": get_sorted_routes(routes),
    }


@router.patch("/game-route/edit-route-positions")
async def edit_route_positions(organized_routes_list: Optional[list[str]]):
    with open(f"temp/routes.json", encoding="utf-8") as routes_file:
        routes = json.load(routes_file)
        routes_file.close()

    for index, name in enumerate(organized_routes_list):
        routes[name]["position"] = index + 1

    with open(f"temp/routes.json", "w", encoding="utf-8") as routes_file:
        routes_file.write(json.dumps(routes))
        routes_file.close()

    return {
        "message": "Route positions edited",
        "status": 200,
        "routes": get_sorted_routes(routes),
    }
