from fastapi import APIRouter
from models.matchup_models import POKEMON_TYPES, pokemon_types, gen_default
from functools import reduce

router = APIRouter()


def create_matchup_map():
    matchup_map = {}
    data = gen_default
    for row_index, row_value in enumerate(data):
        for col_index, col_value in enumerate(row_value):
            type_one = pokemon_types[row_index]
            type_two = pokemon_types[col_index]
            key = f"{type_one} > {type_two}"
            matchup_map[key] = col_value

    return matchup_map


def matchupForPair(generation, defense_type, offense_type):
    # consider storging matchup map for easier access
    # rather than recreating it every time
    matchup_map = create_matchup_map()
    key = f"{offense_type} > {defense_type}"
    value = matchup_map[key]
    return value


def matchupFor(generation, defense_types, offense_type):
    filtered_defense_types = filter(
        lambda defense_type: defense_type != POKEMON_TYPES.none, defense_types
    )
    mapped_defense_types = map(
        lambda defense_type: matchupForPair(generation, defense_type, offense_type),
        filtered_defense_types,
    )
    return reduce(lambda x, y: x * y, mapped_defense_types, 1)


def generate_defensive_matchups(generation, defense_types, pokemon_type):
    effectiveness = matchupFor(generation, defense_types, pokemon_type)
    return {
        "generation": generation,
        "pokemon_type": pokemon_type,
        "effectiveness": effectiveness,
    }


def defensive_matchups(generation: int, defense_types: list):
    matchups = map(
        lambda pokemon_type: generate_defensive_matchups(
            generation, defense_types, pokemon_type
        ),
        pokemon_types,
    )
    return matchups


def group_matchups_by_effectiveness(matchups, effectiveness):
    filtered_matchups = filter(
        lambda matchup: matchup["effectiveness"] == effectiveness, matchups
    )
    mapped_matchups = map(lambda matchup: matchup["pokemon_type"], filtered_matchups)
    return mapped_matchups


@router.get("/matchups/defensive")
async def get_defensive_matchups(types: str):
    type_array = types.split()
    effectiveness_levels = [8, 4, 2, 1, 0.5, 0.25, 0.125, 0]

    matchups = list(defensive_matchups(1, type_array))

    matchups_by_effectiveness = {}
    for effectiveness in effectiveness_levels:
        grouped_matchups = group_matchups_by_effectiveness(matchups, effectiveness)
        matchups_by_effectiveness[effectiveness] = list(grouped_matchups)

    filtered_matchups_by_effectiveness = {}
    for key, value in matchups_by_effectiveness.items():
        if len(value) != 0:
            filtered_matchups_by_effectiveness[key] = value

    return filtered_matchups_by_effectiveness
