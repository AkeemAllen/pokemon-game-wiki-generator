from genericpath import isfile
from os import makedirs
import requests
import tqdm
import pokebase
from snakemd import Document


# makedirs("temp/pokemon/",exist_ok=True)
# makedirs("temp/ability/",exist_ok=True)
# makedirs("temp/move/",exist_ok=True)
# makedirs("temp/item/",exist_ok=True)

# def get_pokemon_data_from_dex_number(pokedex_number):
#     pokebase.pokedex(pokedex_number)
#     response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokedex_number}")
#     if response == "Not Found":
#
#     return response.json()
# {
# 	pokemon: dex_number,
# 	changes: {
# 		item,
# 		abilityOne,
# 		abilityTwo,
# 		HP,
# 		Attack,
# 		Special Attack,
# 		Defense,
# 		Special Defense,
# 		Speed,
# 		Total,
# 		TM,
# 		Catch Rate,
#         HM,
#         Base Happiness,
#         Evolution,
#         Type,
#         Max EXP,
#         Base EXP,
#         Stat Total
# 	}
# }


def get_markdown_file_name(pokedex_number):
    file_name = f"00{pokedex_number}"
    if pokedex_number > 9:
        file_name = f"0{pokedex_number}"
    if pokedex_number > 99:
        file_name = f"{pokedex_number}"

    return file_name


def download_pokemon_sprites():
    pokemon_range = range(1, 10)
    for pokedex_number in tqdm.tqdm(pokemon_range):

        pokemon_data = pokebase.pokemon(pokedex_number)
        if isfile(f"docs/img/pokemon/{pokemon_data.name}.png"):
            continue

        front_facing_sprite_image_url = pokemon_data.sprites.front_default

        image_response = requests.get(f"{front_facing_sprite_image_url}")

        with open(f"docs/img/pokemon/{pokemon_data.name}.png", "wb") as pokemon_image_sprite_file:
            pokemon_image_sprite_file.write(image_response.content)
            pokemon_image_sprite_file.close()


def create_pokemon_markdown_files_and_add_front_sprite():
    # if file doesn't exist, create md file as '<pokedex_number> - <pokemon_name>.md'
    pokemon_range = range(1, 10)
    for pokedex_number in tqdm.tqdm(pokemon_range):
        pokemon_data = pokebase.pokemon(pokedex_number)

        pokedex_markdown_file_name = get_markdown_file_name(pokedex_number)

        markdown_file_path = f"docs/pokemons/{pokedex_markdown_file_name}.md"
        sprite_file_path = f"../img/pokemon/{pokemon_data.name}.png"

        if isfile(markdown_file_path):
            continue

        with open(markdown_file_path, 'w') as pokemon_markdown_file:
            pokemon_markdown_file.write(
                f"![{pokemon_data.name}]({sprite_file_path})"
            )
            pokemon_markdown_file.close()

        with open("temp/new_navigation_items.txt", 'a') as navigation_items:
            navigation_items.write(
                f"- {pokedex_markdown_file_name} - {pokemon_data.name.title()}:"
                f" pokemons/{pokedex_markdown_file_name}.md \n"
            )

# create type table
def create_type_table():
    pokemon_data = pokebase.pokemon(3)
    print(pokemon_data.types[0].type.name)
    # return f"| Version | Type |" \
    #        f"| ---|---|" \
    #        f"| All | Fire|"
    # create defenses table
    # create abilities table
    # create base stats table
    # create level up moves table
    # create learnable moves table
    # create encounter table


# for id in tqdm.tqdm(range(1, 234)):
#
#     if isfile(f"temp/ability/{id}.json"):
#         continue
#
#     response = requests.get(f"https://pokeapi.co/api/v2/ability/{id}")
#
#     if response == "Not Found":
#         continue
#
#     fh = open(f"temp/ability/{id}.json", "wb")
#     fh.write(response.content)
#     fh.close()
#
#
# for id in tqdm.tqdm(range(1,1607)):
#
#     if isfile(f"temp/item/{id}.json"):
#         continue
#
#     response = requests.get(f"https://pokeapi.co/api/v2/item/{id}")
#
#     if response == "Not Found":
#         continue
#
#     fh = open(f"temp/item/{id}.json", "wb")
#     fh.write(response.content)
#     fh.close()


if __name__ == "__main__":
    # create_type_table()
    for id in tqdm.tqdm(range(1, 916)):

        response = requests.get(f"https://pokeapi.co/api/v2/move/{id}")
        move_name = response.json()['name']

        if response == "Not Found":
            continue

        if isfile(f"temp/moves/{move_name}.json"):
            continue

        fh = open(f"temp/moves/{move_name}.json", "wb")
        fh.write(response.content)
        fh.close()
