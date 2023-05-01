from fastapi import APIRouter
import json

from models.move_models import MoveDetails


router = APIRouter()


# Get all move names, which is the key of the move dict
@router.get("/moves")
async def get_moves_list():
    with open(f"temp/moves.json", encoding="utf-8") as moves_file:
        moves = json.load(moves_file)
        moves_file.close()

    return list(moves.keys())


# Get move by name
@router.get("/moves/{move_name}")
async def get_moves(move_name: str):
    with open(f"temp/moves.json", encoding="utf-8") as moves_file:
        moves = json.load(moves_file)
        moves_file.close()

    return moves[move_name]


# Save Changes to move
@router.post("/moves/edit/{move_name}")
def save_move_changes(move_details: MoveDetails, move_name: str):
    with open(f"temp/moves.json", encoding="utf-8") as moves_file:
        moves = json.load(moves_file)
        moves_file.close()

    if move_details.power:
        moves[move_name]["power"] = move_details.power

    if move_details.accuracy:
        moves[move_name]["accuracy"] = move_details.accuracy

    if move_details.pp:
        moves[move_name]["pp"] = move_details.pp

    if move_details.type:
        moves[move_name]["type"] = move_details.type

    if move_details.damage_class:
        moves[move_name]["damage_class"] = move_details.damage_class

    with open(f"temp/moves.json", "w") as moves_file:
        moves_file.write(json.dumps(moves))
        moves_file.close()

    with open(f"temp/updates/modified_moves.json", "r+") as moves_changes_file:
        current_changes = json.load(moves_changes_file)
        if move_name not in current_changes["changed_moves"]:
            current_changes["changed_moves"].append(move_name)
            moves_changes_file.seek(0)
            moves_changes_file.truncate()
            moves_changes_file.write(json.dumps(current_changes))
        moves_changes_file.close()

    return {"message": "Changes Saved"}
