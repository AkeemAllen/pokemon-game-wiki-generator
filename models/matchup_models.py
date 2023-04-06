from enum import Enum


class POKEMON_TYPES(Enum):
    normal = "normal"
    fire = "fire"
    water = "water"
    electric = "electric"
    grass = "grass"
    ice = "ice"
    fighting = "fighting"
    poison = "poison"
    ground = "ground"
    flying = "flying"
    psychic = "psychic"
    bug = "bug"
    rock = "rock"
    ghost = "ghost"
    dragon = "dragon"
    dark = "dark"
    steel = "steel"
    fairy = "fairy"
    none = "none"


pokemon_types_legacy = [
    POKEMON_TYPES.normal,
    POKEMON_TYPES.fire,
    POKEMON_TYPES.water,
    POKEMON_TYPES.electric,
    POKEMON_TYPES.grass,
    POKEMON_TYPES.ice,
    POKEMON_TYPES.fighting,
    POKEMON_TYPES.poison,
    POKEMON_TYPES.ground,
    POKEMON_TYPES.flying,
    POKEMON_TYPES.psychic,
    POKEMON_TYPES.bug,
    POKEMON_TYPES.rock,
    POKEMON_TYPES.ghost,
    POKEMON_TYPES.dragon,
    POKEMON_TYPES.dark,
    POKEMON_TYPES.steel,
    POKEMON_TYPES.fairy,
]

pokemon_types = [
    "normal",
    "fire",
    "water",
    "electric",
    "grass",
    "ice",
    "fighting",
    "poison",
    "ground",
    "flying",
    "psychic",
    "bug",
    "rock",
    "ghost",
    "dragon",
    "dark",
    "steel",
    "fairy",
]

_ = 1;
h = 1 / 2;
# x = NaN;

gen_default = [
  [_, _, _, _, _, _, _, _, _, _, _, _, h, 0, _, _, h, _],
  [_, h, h, _, 2, 2, _, _, _, _, _, 2, h, _, h, _, 2, _],
  [_, 2, h, _, h, _, _, _, 2, _, _, _, 2, _, h, _, _, _],
  [_, _, 2, h, h, _, _, _, 0, 2, _, _, _, _, h, _, _, _],
  [_, h, 2, _, h, _, _, h, 2, h, _, h, 2, _, h, _, h, _],
  [_, h, h, _, 2, h, _, _, 2, 2, _, _, _, _, 2, _, h, _],
  [2, _, _, _, _, 2, _, h, _, h, h, h, 2, 0, _, 2, 2, h],
  [_, _, _, _, 2, _, _, h, h, _, _, _, h, h, _, _, 0, 2],
  [_, 2, _, 2, h, _, _, 2, _, 0, _, h, 2, _, _, _, 2, _],
  [_, _, _, h, 2, _, 2, _, _, _, _, 2, h, _, _, _, h, _],
  [_, _, _, _, _, _, 2, 2, _, _, h, _, _, _, _, 0, h, _],
  [_, h, _, _, 2, _, h, h, _, h, 2, _, _, h, _, 2, h, h],
  [_, 2, _, _, _, 2, h, _, h, 2, _, 2, _, _, _, _, h, _],
  [0, _, _, _, _, _, _, _, _, _, 2, _, _, 2, _, h, _, _],
  [_, _, _, _, _, _, _, _, _, _, _, _, _, _, 2, _, h, 0],
  [_, _, _, _, _, _, h, _, _, _, 2, _, _, 2, _, h, _, h],
  [_, h, h, h, _, 2, _, _, _, _, _, _, 2, _, _, _, h, 2],
  [_, h, _, _, _, _, 2, h, _, _, _, _, _, _, 2, 2, h, _],
];