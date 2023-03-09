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
    pokedex_numbers = range(1, 650)
    for dex_number in tqdm.tqdm(pokedex_numbers):

        if isfile(f"temp/pokemon/{dex_number}.json"):
            continue

        response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{dex_number}")

        if response == "Not Found":
            continue

        fh = open(f"temp/pokemon/{dex_number}.json", "wb")
        fh.write(response.content)
        fh.close()


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


if __name__ == "__main__":
    if "--pokemon" in sys.argv:
        prepare_pokemon_data()
    if "--sprites" in sys.argv:
        download_pokemon_sprites()
    if "--moves" in sys.argv:
        prepare_move_data()

