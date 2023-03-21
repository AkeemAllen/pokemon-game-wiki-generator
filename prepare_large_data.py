import json
from genericpath import isfile
from json import JSONDecodeError
import requests
import tqdm
import sys


def get_markdown_file_name(pokedex_number):
    file_name = f"00{pokedex_number}"
    if pokedex_number > 9:
        file_name = f"0{pokedex_number}"
    if pokedex_number > 99:
        file_name = f"{pokedex_number}"

    return file_name


def update_pokemon_data():
    with open("updates/pokemon_changes.json", encoding="utf-8") as pokemon_changes_file:
        pokemon_changes = json.load(pokemon_changes_file)
        pokemon_changes_file.close()

    with open(f"temp/moves.json", encoding='utf-8') as move_json_file:
        moves = json.load(move_json_file)
        move_json_file.close()

    for pokemon_name, pokemon_updates in tqdm.tqdm(pokemon_changes.items()):
        if pokemon_updates["id"] == 0:
            continue

        dex_number = pokemon_updates["id"]
        with open(f"temp/pokemon/{dex_number}.json", encoding="utf-8") as pokemon_file:
            pokemon_data = json.load(pokemon_file)
            pokemon_file.close()

        if "stats" in pokemon_updates:
            for stat in pokemon_data["stats"]:
                stat_name = stat["stat"]["name"]
                stat["base_stat"] = pokemon_updates["stats"][stat_name] if stat_name in pokemon_updates["stats"] else stat[
                    "base_stat"]

        if "abilities" in pokemon_updates:
            pokemon_data["abilities"] = [
                {"ability": {"name": update.title()}} for update in pokemon_updates["abilities"]
            ]

        if "types" in pokemon_updates:
            pokemon_data["types"] = [{"type": {"name": update}} for update in pokemon_updates["types"]]

        if "evolution" in pokemon_updates:
            pokemon_data["evolution"] = pokemon_updates["evolution"]

        if "moves" in pokemon_updates:
            for move in pokemon_updates["moves"]:
                pokemon_data["moves"][move] = {
                    "id": moves[move]["id"],
                    "level_learned_at": pokemon_updates["moves"][move],
                    "learn_method": "level-up"
                }

        if "machine_moves" in pokemon_updates:
            for machine_move in pokemon_updates["machine_moves"]:
                pokemon_data["moves"][machine_move] = {
                    "id": moves[machine_move]["id"],
                    "level_learned_at": 0,
                    "learn_method": "machine"
                }

        with open(f"temp/pokemon/{dex_number}.json", "w") as pokemon_file:
            pokemon_file.write(json.dumps(pokemon_data))
            pokemon_file.close()


def prepare_move_data():
    move_range = range(1, 903)
    moves = {}
    for move_id in tqdm.tqdm(move_range):

        response = requests.get(f"https://pokeapi.co/api/v2/move/{move_id}")
        if response == "Not Found":
            continue

        try:
            move = response.json()
        except JSONDecodeError as err:
            print(f"Move with id {move_id} failed: {err}")
            continue

        moves[move["name"]] = {
            "id": move_id,
            "power": move["power"],
            "type": move["type"]["name"],
            "accuracy": move["accuracy"],
            "pp": move["pp"],
            "damage_class": move["damage_class"]["name"],
            "past_values": move["past_values"]
        }

    fh = open(f"temp/moves.json", "w")
    fh.write(json.dumps(moves))
    fh.close()


def download_pokemon_data():
    pokedex_numbers = range(1, 200)

    for dex_number in tqdm.tqdm(pokedex_numbers):

        # if isfile(f"temp/pokemon/{dex_number}.json"):
        #     continue

        response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{dex_number}")

        if response == "Not Found":
            continue

        pokemon_data = response.json()
        moves = {}
        # transform pokemon moves to make manipulating the data easier
        for index, move in enumerate(pokemon_data["moves"]):
            group_details = move["version_group_details"]
            move_details = None
            for detail in group_details:
                if detail["version_group"]["name"] == "black-white":
                    move_details = detail
                    break

            if move_details is None:
                continue

            move_name = move["move"]["name"]
            move_id = move["move"]["url"].split("/")[-2]
            moves[move_name] = {
                "id": move_id,
                "level_learned_at": move_details["level_learned_at"],
                "learn_method": move_details["move_learn_method"]["name"],
            }

        pokemon_data["moves"] = moves
        with open(f"temp/pokemon/{dex_number}.json", "w") as pokemon_file:
            pokemon_file.write(json.dumps(pokemon_data))
            pokemon_file.close()


def download_pokemon_sprites():
    pokemon_range = range(1, 650)
    for pokedex_number in tqdm.tqdm(pokemon_range):
        image_file_name = get_markdown_file_name(pokedex_number)
        if isfile(f"docs/img/pokemon/{image_file_name}.png"):
            continue

        with open(f"temp/pokemon/{pokedex_number}.json", encoding='utf-8') as pokemon_data_file:
            pokemon_data = json.load(pokemon_data_file)
            front_facing_sprite_image_url = pokemon_data['sprites']['front_default']

        image_response = requests.get(f"{front_facing_sprite_image_url}")

        with open(f"docs/img/pokemon/{image_file_name}.png", "wb") as pokemon_image_sprite_file:
            pokemon_image_sprite_file.write(image_response.content)
            pokemon_image_sprite_file.close()


def prepare_technical_and_hidden_machines_data():
    machine_range = range(1, 1689)
    machines = {}
    for machine_id in tqdm.tqdm(machine_range):

        response = requests.get(f"https://pokeapi.co/api/v2/machine/{machine_id}")

        if response == "Not Found":
            continue

        machine_data = response.json()
        machine_name = machine_data["move"]["name"]

        if machine_name not in machines:
            machines[machine_name] = []

        machines[machine_data["move"]["name"]].append({
            "technical_name": machine_data["item"]["name"],
            "game_version": machine_data["version_group"]["name"]
        })
    # Might be a better idea to append each new machine to the file
    # rather downloading all at once and then storing in file
    # That approach would likely be more tolerant of any faults that
    # may arise on the network side
    with open(f"temp/machines.json", "w") as machine_data_file:
        machine_data_file.write(json.dumps(machines))
        machine_data_file.close()
    print(machines)


if __name__ == "__main__":
    if "--pokemon" in sys.argv:
        download_pokemon_data()
    if "--sprites" in sys.argv:
        download_pokemon_sprites()
    if "--moves" in sys.argv:
        prepare_move_data()
    if "--machines" in sys.argv:
        prepare_technical_and_hidden_machines_data()
    if "--update" in sys.argv:
        update_pokemon_data()

