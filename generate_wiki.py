import os
import shutil
import json
import argparse
import yaml

# focus on generating more general wiki pages. I.e. changes to pokemon, moves, trainers, encounters
# focus on pokemon for now


def generate_yaml(
    wiki_name: str = "Rom Hack Wiki",
    wiki_description: str = "Rom Hack Documentation",
    wiki_author: str = "Rom Hackers",
    repo_url: str = "https://placeholder.com",
    site_url: str = "https://placeholder.com",
):
    mkdocs_yaml_dict = {
        "site_name": f"{wiki_name}",
        "site_url": f"{site_url}",
        "site_description": f"{wiki_description}",
        "site_author": f"{wiki_author}",
        "repo_url": f"{repo_url}",
        "theme": {
            "palette": [
                {
                    "media": "(prefers-color-scheme: light)",
                    "primary": "black",
                    "scheme": "default",
                    "toggle": {
                        "icon": "material/eye-outline",
                        "name": "Switch to dark mode",
                    },
                },
                {
                    "media": "(prefers-color-scheme: dark)",
                    "primary": "black",
                    "scheme": "slate",
                    "toggle": {"icon": "material/eye", "name": "Switch to light mode"},
                },
            ],
            "name": "material",
            "favicon": "img/items/poke-ball.png",
            "features": ["content.tabs.link"],
        },
        "nav": [
            {"Home": "index.md"},
            {
                "Pokémons": [
                    {"Evolution Changes": "pokemons/evolution_changes.md"},
                    {"Specific Changes": [{"001 - Bulbasaur": "pokemons/001.md"}]},
                ]
            },
        ],
        "plugins": [{"search": {"lang": "en"}}],
    }

    return mkdocs_yaml_dict


def create_boiler_plate(wiki_name: str):
    base_path = f"dist/{wiki_name}"

    if os.path.exists(base_path):
        print("Wiki already exists. Exiting...")
        return

    # image folders
    shutil.copytree("generator_assets/items", f"{base_path}/docs/img/items")
    shutil.copytree("generator_assets/types", f"{base_path}/docs/img/types")
    os.makedirs(f"{base_path}/docs/img/pokemon")

    # pokemon folder
    os.makedirs(f"{base_path}/docs/pokemon")

    with open(f"{base_path}/docs/index.md", "w") as markdown_index_file:
        markdown_index_file.write("# Index")
        markdown_index_file.close()

    config = {
        "useSideMenu": True,
        "lineBreaks": "gfm",
        "anchorCharacter": "#",
        "title": "Blaze Black Wiki",
    }

    with open(f"{base_path}/docs/config.json", "w") as config_file:
        config_file.write(json.dumps(config))
        config_file.close()

    mkdocs_yaml = generate_yaml(wiki_name)

    with open(f"{base_path}/mkdocs.yml", "w") as mkdocs_yaml_file:
        yaml.dump(mkdocs_yaml, mkdocs_yaml_file, sort_keys=False, indent=4)
        mkdocs_yaml_file.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--name", help="Name of wiki")

    args = parser.parse_args()

    create_boiler_plate(args.name)


if __name__ == "__main__":
    main()
