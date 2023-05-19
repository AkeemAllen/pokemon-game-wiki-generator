from fastapi import APIRouter
import json

router = APIRouter()


# Get all pokemon and return by dict with name and id
@router.get("/abilities")
async def get_item_list():
    with open(f"temp/abilities.json", encoding="utf-8") as abilities_file:
        abilities = json.load(abilities_file)
        abilities_file.close()

    return [ability_name for ability_name, _ in abilities.items()]
