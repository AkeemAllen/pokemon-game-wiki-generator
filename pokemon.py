import json
from collections import defaultdict

import pokebase
from genericpath import isfile
import requests
import tqdm
from snakemd import Document, InlineText, Table, Paragraph


def get_markdown_image_for_type(_type: str):
    return f"![{_type}](../img/types/{_type}.png)"


def get_markdown_file_name(pokedex_number):
    file_name = f"00{pokedex_number}"
    if pokedex_number > 9:
        file_name = f"0{pokedex_number}"
    if pokedex_number > 99:
        file_name = f"{pokedex_number}"

    return file_name


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
        # print(response)
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

        for stat in data["stats"]:
            stats[stat["stat"]["name"]] = stat["base_stat"]

        doc.add_header("Base Stats", 2)
        doc.add_table(
            ["Version", "HP", "Atk", "Def", "SAtk", "SDef", "Spd"],
            [
                [
                    "All",
                    stats.get("hp"),
                    stats.get("attack"),
                    stats.get("defense"),
                    stats.get("special-attack"),
                    stats.get("special-defense"),
                    stats.get("speed")]
            ]
        )

    def create_level_up_moves_table(self, doc: Document, version_group: str):
        data = self.pokemon_data
        moves = {}
        # for details in data.moves.version_group_details:
        #     if details.version_group.name == version_group:
        #         print(details.version_group.name)
        for move in data["moves"]:
            move_id = move["move"]["url"].split("/")[-2]
            with open(f"temp/moves/{move_id}.json", encoding='utf-8') as move_details_file:
                move_details = json.load(move_details_file)
                move_details_file.close()

            level_learned = ""
            group_details = move["version_group_details"]
            for detail in group_details:
                if detail["version_group"]["name"] == version_group:
                    level_learned = detail["level_learned_at"]

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

        table_array_for_moves = []
        for move_name, move_attributes in sorted_moves.items():
            move_array = [
                move_attributes.get("level_learned"),
                move_name.title(),
                move_attributes.get("power") if move_attributes.get("power") else "-",
                f"{move_attributes.get('accuracy')}%" if move_attributes.get("accuracy") else "-",
                move_attributes.get("pp") if move_attributes.get("pp") else "-",
                f"{get_markdown_image_for_type(move_attributes.get('type'))}",
                f"{get_markdown_image_for_type(move_attributes.get('damage_class'))}",
            ]
            table_array_for_moves.append(move_array)

        doc.add_header("Level Up Moves", 2)
        doc.add_table(
            ["Level", "Name", "Power", "Accuracy", "PP", "Type", "Damage Class"],
            table_array_for_moves
        )


def main():
    pokemon_range = range(1, 2)
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

        doc.output_page(markdown_file_path)
        # pokemon.create_defenses_table(doc)


if __name__ == "__main__":
    main()


