from models.game_route_models import TrainerOrWildPokemon


def get_pokemon_dex_formatted_name(pokedex_number):
    file_name = f"00{pokedex_number}"
    if pokedex_number > 9:
        file_name = f"0{pokedex_number}"
    if pokedex_number > 99:
        file_name = f"{pokedex_number}"

    return file_name


def get_sorted_routes(routes):
    return dict(sorted(routes.items(), key=lambda route: route[1]["position"]))


def get_markdown_image_for_item(item_name: str):
    if item_name == "" or item_name is None:
        return ""
    return f"![{item_name}](../../img/items/{item_name}.png)"


def get_markdown_image_for_pokemon(pokemon_list, pokemon_name: str):
    dex_number = pokemon_list[pokemon_name]["id"]
    file_name = get_pokemon_dex_formatted_name(dex_number)
    return f"![{pokemon_name}](../../img/pokemon/{file_name}.png)"


def get_link_to_pokemon_page(pokemon_list, pokemon_name: str):
    dex_number = pokemon_list[pokemon_name]["id"]
    url_route = get_pokemon_dex_formatted_name(dex_number)
    return f"[{pokemon_name.capitalize()}](/blaze-black-wiki/pokemon/{url_route})"


def generate_move_string(moves):
    move_string = ""
    if moves is None or len(moves) == 0:
        return f"<ul><li>N/A</li><li>N/A</li><li>N/A</li><li>N/A</li></ul>"

    for move in moves:
        move_string += f"<li>{move.title() if move else 'N/A'}</li>"

    return f"<ul>{move_string}</ul>"


def get_bottom_value_for_pokemon(
    pokemon: TrainerOrWildPokemon, is_trainer_mapping=False
):
    bottom_value = ""
    if is_trainer_mapping:
        bottom_value = f"Lv. {pokemon.level}"
    else:
        bottom_value = f"{pokemon.encounter_rate}%"

    return bottom_value
