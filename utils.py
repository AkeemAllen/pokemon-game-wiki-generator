def get_pokemon_dex_formatted_name(pokedex_number):
    file_name = f"00{pokedex_number}"
    if pokedex_number > 9:
        file_name = f"0{pokedex_number}"
    if pokedex_number > 99:
        file_name = f"{pokedex_number}"

    return file_name


def get_sorted_routes(routes):
    return dict(sorted(routes.items(), key=lambda route: route[1]["position"]))
