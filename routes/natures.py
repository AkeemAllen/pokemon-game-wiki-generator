from fastapi import APIRouter
import json

router = APIRouter()


# Get all pokemon and return by dict with name and id
@router.get("/natures")
async def get_item_list():
    with open(f"temp/natures.json", encoding="utf-8") as natures_file:
        natures = json.load(natures_file)
        natures_file.close()

    return natures
