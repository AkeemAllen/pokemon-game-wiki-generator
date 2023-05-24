import os
import shutil
import json
import argparse
import yaml

# focus on generating more general wiki pages. I.e. changes to pokemon, moves, trainers, encounters
# focus on pokemon for now


def generate_yaml(
    site_name: str = "Rom Hack Wiki",
    wiki_name: str = "Rom Hack Wiki",
    wiki_description: str = "Rom Hack Documentation",
    wiki_author: str = "Rom Hackers",
    repo_url: str = "https://placeholder.com",
    site_url: str = "https://placeholder.com",
):
    mkdocs_yaml_dict = {
        "site_name": f"{site_name}",
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
                "Pokemon": [
                    {"Specific Changes": [{"Test Pokemon": "pokemon/test_pokemon.md"}]},
                ],
            },
            {
                "Routes": [
                    {
                        "Test route": [
                            {"Wild Encounters": "routes/Test_route/wild_encounters.md"}
                        ]
                    }
                ]
            },
        ],
        "plugins": [{"search": {"lang": "en"}}],
        "markdown_extensions": [
            {"pymdownx.tasklist": {"custom_checkbox": True}},
            "pymdownx.superfences",
            {"pymdownx.tabbed": {"alternate_style": True}},
        ],
    }

    return mkdocs_yaml_dict


def create_boiler_plate(
    wiki_name: str, wiki_description: str, wiki_author: str, site_name: str
):
    base_path = f"dist/{wiki_name}"

    if os.path.exists(base_path):
        print("Wiki already exists. Exiting...")
        return

    # image folders
    shutil.copytree("generator_assets/items", f"{base_path}/docs/img/items")
    shutil.copytree("generator_assets/types", f"{base_path}/docs/img/types")
    os.makedirs(f"{base_path}/docs/img/pokemon")

    # pokemon folder with an placeholder pokemon file
    os.makedirs(f"{base_path}/docs/pokemon")

    with open(f"{base_path}/docs/pokemon/test_pokemon.md", "w") as markdown_file:
        markdown_file.write("# Placeholder Pokemon")
        markdown_file.close()

    # routes folder with an placeholder route folder and file
    os.makedirs(f"{base_path}/docs/routes/Test_route")

    with open(
        f"{base_path}/docs/routes/Test_route/wild_encounters.md", "w"
    ) as markdown_file:
        markdown_file.write("# Wild Encounters")
        markdown_file.close()

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

    repo_url = f"https://github.com/{wiki_author}/{wiki_name}"
    site_url = f"https://{wiki_author.lower()}.github.io/{wiki_name}"

    mkdocs_yaml = generate_yaml(
        site_name, wiki_name, wiki_description, wiki_author, repo_url, site_url
    )

    with open(f"{base_path}/mkdocs.yml", "w") as mkdocs_yaml_file:
        yaml.dump(mkdocs_yaml, mkdocs_yaml_file, sort_keys=False, indent=4)
        mkdocs_yaml_file.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--name", help="Name of wiki")
    parser.add_argument("-d", "--description", help="Description of wiki")
    parser.add_argument(
        "-a",
        "--author",
        help="Author of wiki (use your github username so site generation can be more accurate)",
    )
    parser.add_argument("-s", "--site-name", help="Site name of wiki")

    args = parser.parse_args()

    create_boiler_plate(args.name, args.description, args.author, args.site_name)


if __name__ == "__main__":
    main()
