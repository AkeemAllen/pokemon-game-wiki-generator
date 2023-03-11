import json
from genericpath import isfile
from os import makedirs
import requests
import tqdm
import sys
import pokebase


def get_markdown_file_name(pokedex_number):
    file_name = f"00{pokedex_number}"
    if pokedex_number > 9:
        file_name = f"0{pokedex_number}"
    if pokedex_number > 99:
        file_name = f"{pokedex_number}"

    return file_name


def prepare_move_data():
    move_range = range(1, 916)
    for move_id in tqdm.tqdm(move_range):

        if isfile(f"temp/moves/{move_id}.json"):
            continue

        response = requests.get(f"https://pokeapi.co/api/v2/move/{move_id}")

        if response == "Not Found":
            continue

        fh = open(f"temp/moves/{move_id}.json", "wb")
        fh.write(response.content)
        fh.close()


def prepare_pokemon_data():
    pokedex_numbers = range(1, 2)

    with open("updates/pokemon_changes.json", encoding="utf-8") as pokemon_changes_file:
        pokemon_changes = json.load(pokemon_changes_file)
        pokemon_changes_file.close()

    for dex_number in tqdm.tqdm(pokedex_numbers):

        # if isfile(f"temp/pokemon/{dex_number}.json"):
        #     continue

        response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{dex_number}")

        if response == "Not Found":
            continue

        pokemon_data = response.json()
        if pokemon_data["name"] not in pokemon_changes:
            continue

        if "stats" in pokemon_changes[pokemon_data["name"]]:
            for stat in pokemon_data["stats"]:
                stat_name = stat["stat"]["name"]
                updates = pokemon_changes[pokemon_data["name"]]
                stat["base_stat"] = updates["stats"][stat_name] if stat_name in updates["stats"] else stat["base_stat"]

        # fh = open(f"temp/pokemon/{dex_number}.json", "wb")
        # fh.write(response.content)
        # fh.close()


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
        prepare_pokemon_data()
    if "--sprites" in sys.argv:
        download_pokemon_sprites()
    if "--moves" in sys.argv:
        prepare_move_data()
    if "--machines" in sys.argv:
        prepare_technical_and_hidden_machines_data()

