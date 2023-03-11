import json
from collections import defaultdict

import pokebase
from genericpath import isfile
import requests
import tqdm
from snakemd import Document, InlineText, Table, Paragraph
from enum import Enum


class PokemonVersions (Enum):
    RED_BLUE = "red-blue"
    YELLOW = "yellow"
    GOLD_SILVER = "gold-silver"
    CRYSTAL = "crystal"
    RUBY_SAPPHIRE = "ruby-sapphire"
    EMERALD = "emerald"
    FIRERED_LEAFGREEN = "firered-leafgreen"
    DIAMOND_PEARL = "diamond-pearl"
    PLATINUM = "platinum"
    HEARTGOLD_SOULSILVER = "heartgold-soulsilver"
    BLACK_WHITE = "black-white"
    BLACKTWO_WHITETWO = "black-2-white-2"
    X_Y = "x-y"
    OMEGARUBY_ALPHASAPPHIRE = "omega-ruby-alpha-sapphire"
    SUN_MOON = "sun-moon"
    ULTRASUN_ULTRAMOON = "ultra-sun-ultra-moon"
    SWORD_SHEILD = "sword-shield"


pokemon_versions_ordered = {
    PokemonVersions.RED_BLUE: 0,
    PokemonVersions.YELLOW: 1,
    PokemonVersions.GOLD_SILVER: 2,
    PokemonVersions.CRYSTAL: 3,
    PokemonVersions.RUBY_SAPPHIRE: 4,
    PokemonVersions.EMERALD: 5,
    PokemonVersions.FIRERED_LEAFGREEN: 6,
    PokemonVersions.DIAMOND_PEARL: 7,
    PokemonVersions.BLACK_WHITE: 8,
    PokemonVersions.BLACKTWO_WHITETWO: 9,
    PokemonVersions.X_Y: 10,
    PokemonVersions.OMEGARUBY_ALPHASAPPHIRE: 11,
    PokemonVersions.SUN_MOON: 12,
    PokemonVersions.ULTRASUN_ULTRAMOON: 13,
    PokemonVersions.SWORD_SHEILD: 14
}


def get_markdown_image_for_type(_type: str):
    return f"![{_type}](../img/types/{_type}.png)"


def get_markdown_file_name(pokedex_number):
    file_name = f"00{pokedex_number}"
    if pokedex_number > 9:
        file_name = f"0{pokedex_number}"
    if pokedex_number > 99:
        file_name = f"{pokedex_number}"

    return file_name


def generate_moves_array(moves, table_type):
    table_array_for_moves = []
    for move_name, move_attributes in moves.items():
        move_array = [
            move_attributes.get("level_learned" if table_type == "level_up" else "machine"),
            move_name.title(),
            move_attributes.get("power") if move_attributes.get("power") else "-",
            f"{move_attributes.get('accuracy')}%" if move_attributes.get("accuracy") else "-",
            move_attributes.get("pp") if move_attributes.get("pp") else "-",
            f"{get_markdown_image_for_type(move_attributes.get('type'))}",
            f"{get_markdown_image_for_type(move_attributes.get('damage_class'))}",
        ]
        table_array_for_moves.append(move_array)
    return table_array_for_moves


class Pokemon:
    def __init__(self, dex_number):
        self.pokemon_data = None
        self.dex_number = dex_number

    def get_pokemon_data(self):
        with open(f"temp/pokemon/{self.dex_number}.json", encoding='utf-8') as pokemon_data_file:
            self.pokemon_data = json.load(pokemon_data_file)
            pokemon_data_file.close()
        return self.pokemon_data

    def add_sprite(self, doc: Document):
        doc.add_element(
            Paragraph(
                [InlineText(
                    f"{self.pokemon_data['name']}", url=f"../img/pokemon/{get_markdown_file_name(self.dex_number)}.png", image=True
                )]
            ))

    def create_type_table(self, doc: Document):
        data = self.pokemon_data
        type_images = [get_markdown_image_for_type(_type["type"]["name"]) for _type in data["types"]]

        doc.add_header("Types", 2)
        doc.add_table(
            ["Version", "Type"],
            [
                ["Classic", " ".join(map(str, type_images))]
            ],
            [Table.Align.CENTER, Table.Align.RIGHT],
            0
        )

    def create_defenses_table(self, doc: Document):
        data = self.pokemon_data
        types = [_type["type"]["name"] for _type in data["types"]]
        query_string = f"{types[0]}+{types[1]}" if len(types) > 1 else f"{types[0]}"

        response = requests.get(f"http://localhost:3000?types={query_string}").json()
        immunities = ""
        normal_resists = ""
        two_weak_resists = ""
        four_weak_resists = ""
        half_strong_resists = ""
        quarter_strong_resists = ""

        if "0" in response:
            immunities = [get_markdown_image_for_type(pokemon_type) for pokemon_type in response['0']]

        if "1" in response:
            normal_resists = [get_markdown_image_for_type(pokemon_type) for pokemon_type in response['1']]

        if "2" in response:
            two_weak_resists = [get_markdown_image_for_type(pokemon_type) for pokemon_type in response['2']]

        if "4" in response:
            four_weak_resists = [get_markdown_image_for_type(pokemon_type) for pokemon_type in response['4']]

        if "0.5" in response:
            half_strong_resists = [get_markdown_image_for_type(pokemon_type) for pokemon_type in response['0.5']]

        if "0.25" in response:
            quarter_strong_resists = [get_markdown_image_for_type(pokemon_type) for pokemon_type in response['0.25']]

        doc.add_header("Defenses", 2)
        doc.add_table(
            ["Immune x0", "Resistant ×¼", "Resistant ×½", "Normal ×1", "Weak ×2", "Weak ×4"],
            [
                [
                    "<br/>".join(map(str, immunities)),
                    "<br/>".join(map(str, quarter_strong_resists)),
                    "<br/>".join(map(str, half_strong_resists)),
                    "<br/>".join(map(str, normal_resists)),
                    "<br/>".join(map(str, two_weak_resists)),
                    "<br/>".join(map(str, four_weak_resists))
                ]
            ]
        )
        return

    def create_ability_table(self, doc: Document):
        data = self.pokemon_data
        abilities = [ability["ability"]["name"].title() for ability in data["abilities"]]

        doc.add_header("Abilities", 2)
        doc.add_table(
            ["Version", "Ability"],
            [
                ["All", " / ".join(map(str, abilities))]
            ]
        )

    def create_stats_table(self, doc: Document):
        data = self.pokemon_data
        stats = {}

        base_stat_total = 0
        for stat in data["stats"]:
            stats[stat["stat"]["name"]] = stat["base_stat"]
            base_stat_total += stat["base_stat"]

        doc.add_header("Base Stats", 2)
        doc.add_table(
            ["Version", "HP", "Atk", "Def", "SAtk", "SDef", "Spd", "BST"],
            [
                [
                    "All",
                    stats.get("hp"),
                    stats.get("attack"),
                    stats.get("defense"),
                    stats.get("special-attack"),
                    stats.get("special-defense"),
                    stats.get("speed"),
                    base_stat_total
                ]
            ]
        )

    def create_level_up_moves_table(self, doc: Document, version_group: str):
        data = self.pokemon_data
        moves = {}

        for move in data["moves"]:
            group_details = move["version_group_details"]
            if group_details[0]["move_learn_method"]["name"] != "level-up":
                continue

            move_id = move["move"]["url"].split("/")[-2]
            with open(f"temp/moves/{move_id}.json", encoding='utf-8') as move_details_file:
                move_details = json.load(move_details_file)
                move_details_file.close()

            level_learned = ""
            for detail in group_details:
                if detail["version_group"]["name"] == version_group:
                    level_learned = detail["level_learned_at"]
                    relevant_past_value = [
                        value for value in move_details["past_values"] if value["version_group"]["name"] == version_group
                    ]
                    if len(relevant_past_value) > 0:
                        move_details["accuracy"] = relevant_past_value[0]["accuracy"] or move_details["accuracy"]
                        move_details["power"] = relevant_past_value[0]["power"] or move_details["power"]
                        move_details["pp"] = relevant_past_value[0]["power"] or move_details["pp"]
                        move_details["type"] = relevant_past_value[0]["type"] or move_details["type"]
                    break

            if level_learned == "" or level_learned == 0:
                continue

            moves[move["move"]["name"]] = {
                "level_learned": level_learned,
                "power": move_details["power"],
                "type": move_details["type"]["name"],
                "accuracy": move_details["accuracy"],
                "pp": move_details["pp"],
                "damage_class": move_details["damage_class"]["name"],
            }

        sorted_moves = dict(sorted(moves.items(), key=lambda x: x[1]["level_learned"], reverse=False))

        doc.add_header("Level Up Moves", 2)
        doc.add_table(
            ["Level", "Name", "Power", "Accuracy", "PP", "Type", "Damage Class"],
            generate_moves_array(sorted_moves, table_type="level_up")
        )

    def create_learnable_moves(self, doc: Document, version_group: str):
        data = self.pokemon_data
        moves = {}

        with open("temp/machines.json", encoding='utf-8') as machines_file:
            machines = json.load(machines_file)
            machines_file.close()

        for move in data["moves"]:
            if move["move"]["name"] not in machines:
                continue

            group_details = move["version_group_details"]
            if group_details[0]["move_learn_method"]["name"] != "machine":
                continue

            move_id = move["move"]["url"].split("/")[-2]
            with open(f"temp/moves/{move_id}.json", encoding='utf-8') as move_details_file:
                move_details = json.load(move_details_file)
                move_details_file.close()

            machine_name = ""
            for machine_version in machines[move["move"]["name"]]:
                if machine_version["game_version"] == version_group:
                    machine_name = machine_version["technical_name"]
                    break

            if machine_name == "":
                continue

            moves[move["move"]["name"]] = {
                "machine": machine_name.upper(),
                "power": move_details["power"],
                "type": move_details["type"]["name"],
                "accuracy": move_details["accuracy"],
                "pp": move_details["pp"],
                "damage_class": move_details["damage_class"]["name"],
            }

        sorted_moves = dict(sorted(moves.items(), key=lambda x: x[1]["machine"], reverse=False))

        doc.add_header("Learnable Moves", 2)
        doc.add_table(
            ["Machine", "Name", "Power", "Accuracy", "PP", "Type", "Damage Class"],
            generate_moves_array(sorted_moves, table_type="learnable")
        )


def main():
    pokemon_range = range(1, 20)
    for pokedex_number in tqdm.tqdm(pokemon_range):
        pokemon = Pokemon(pokedex_number)
        pokemon_data = pokemon.get_pokemon_data()

        pokedex_markdown_file_name = get_markdown_file_name(pokedex_number)

        markdown_file_path = f"docs/pokemons/"

        doc = Document(pokedex_markdown_file_name)

        doc.add_header(f"{pokedex_markdown_file_name} - {pokemon_data['name'].title()}")

        pokemon.add_sprite(doc)
        pokemon.create_type_table(doc)
        pokemon.create_defenses_table(doc)
        pokemon.create_ability_table(doc)
        pokemon.create_stats_table(doc)
        pokemon.create_level_up_moves_table(doc, version_group="black-white")
        pokemon.create_learnable_moves(doc, version_group="black-white")

        doc.output_page(markdown_file_path)

        with open("temp/new_navigation_items.txt", 'a') as navigation_items:
            navigation_items.write(
                f"- {pokedex_markdown_file_name} - {pokemon_data['name'].title()}:"
                f" pokemons/{pokedex_markdown_file_name}.md \n"
            )
            navigation_items.close()


if __name__ == "__main__":
    main()



