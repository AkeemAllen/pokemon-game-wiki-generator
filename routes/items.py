from fastapi import APIRouter
import json

router = APIRouter()


# Get all pokemon and return by dict with name and id
@router.get("/items")
async def get_item_list():
    with open(f"temp/items.json", encoding="utf-8") as items_file:
        items = json.load(items_file)
        items_file.close()

    return [item_name for item_name, _ in items.items()]
