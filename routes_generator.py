import argparse
import json
import os
import pokebase
import yaml
from snakemd import Document

from utils import get_pokemon_dex_formatted_name


with open(f"temp/pokemon.json", encoding="utf-8") as pokemon_file:
    pokemon = json.load(pokemon_file)
    pokemon_file.close()


def get_markdown_image_for_item(item_name: str):
    return f"![{item_name}](../../img/items/{item_name}.png)"


def get_markdown_image_for_pokemon(pokemon_name: str):
    dex_number = pokemon[pokemon_name]["id"]
    file_name = get_pokemon_dex_formatted_name(dex_number)
    return f"![{pokemon_name}](../../img/pokemon/{file_name}.png)"


def get_link_to_pokemon_page(pokemon_name: str):
    dex_number = pokemon[pokemon_name]["id"]
    url_route = get_pokemon_dex_formatted_name(dex_number)
    return f"[{pokemon_name}](/pokemon/{url_route})"


def get_encounter_table_columns(max_pokemon_on_single_route):
    table_columns = ["Area", "Pokemon"]
    if max_pokemon_on_single_route == 1:
        return table_columns

    for i in range(max_pokemon_on_single_route - 1):
        if i < 5:
            table_columns.append("&nbsp;")
    return table_columns


def map_encounter_to_markdown(encounter_list):
    encounter_list_markdown = map(
        lambda encounter: f"{get_markdown_image_for_pokemon(encounter[0])}<br/>{get_link_to_pokemon_page(encounter[0])}<br/>{encounter[1]}%",
        encounter_list,
    )
    encounter_list_markdown = list(encounter_list_markdown)
    return encounter_list_markdown


def get_encounter_table_rows(encounters):
    max_number_of_pokemon_on_single_route = 0
    table_array_rows_for_encounters = []

    for encounter_type, pokemon_encounter_list in encounters.items():
        if len(pokemon_encounter_list[:-1]) > max_number_of_pokemon_on_single_route:
            max_number_of_pokemon_on_single_route = len(pokemon_encounter_list[:-1])

        mapped_encounter_list = map_encounter_to_markdown(pokemon_encounter_list[:-1])
        extra_encounter_array = []
        extra_encounter_list = []

        if len(mapped_encounter_list) > 6:
            extra_encounter_list = mapped_encounter_list[6:]
            mapped_encounter_list = mapped_encounter_list[:6]
            extra_encounter_array = [f"", *extra_encounter_list]

        encounter_array = [
            f"{get_markdown_image_for_item(encounter_type)}<br/>old rod<br/>{encounters[encounter_type][-1]}",
            *mapped_encounter_list,
        ]

        table_array_rows_for_encounters.append(encounter_array)
        if extra_encounter_array:
            table_array_rows_for_encounters.append(extra_encounter_array)

    return (
        table_array_rows_for_encounters,
        max_number_of_pokemon_on_single_route,
    )


def create_encounter_table(route_name: str, route_directory: str, encounters):
    doc = Document("wild_encounters")
    doc.add_header(f"{route_name.capitalize()}", 1)
    table_rows, max_number_of_pokemon_on_single_route = get_encounter_table_rows(
        encounters
    )

    table_columns = get_encounter_table_columns(max_number_of_pokemon_on_single_route)

    doc.add_table(
        table_columns,
        table_rows,
    )

    doc.output_page(f"{route_directory}/")


def main(wiki_name: str):
    with open(f"dist/{wiki_name}/mkdocs.yml", "r") as mkdocs_file:
        mkdocs_yaml_dict = yaml.load(mkdocs_file, Loader=yaml.FullLoader)
        mkdocs_file.close()

    with open(f"temp/routes.json", encoding="utf-8") as routes_file:
        routes = json.load(routes_file)
        routes_file.close()

    mkdoc_routes = mkdocs_yaml_dict["nav"][2]["Routes"]
    for route_name, route_properties in routes.items():
        route_directory = f"dist/{wiki_name}/docs/routes/{route_name}"
        if not os.path.exists(route_directory):
            os.makedirs(route_directory)

        create_encounter_table(
            route_name, route_directory, route_properties["encounters"]
        )

        route_entry = {
            route_name.replace("_", " ").capitalize(): [
                {"Wild Encounters": f"routes/{route_name}/wild_encounters.md"}
            ]
        }

        if route_entry not in mkdoc_routes:
            mkdoc_routes.append(route_entry)

    mkdocs_yaml_dict["nav"][2]["Routes"] = mkdoc_routes

    with open(f"dist/{wiki_name}/mkdocs.yml", "w") as mkdocs_file:
        yaml.dump(mkdocs_yaml_dict, mkdocs_file, sort_keys=False, indent=4)
        mkdocs_file.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-wn",
        "--wiki-name",
        help="Specify the name of the wiki to download data from",
        type=str,
    )

    args = parser.parse_args()

    main(args.wiki_name)
