class PHASES:
    PREGAMEPHASE = 0
    PLANNINGPHASE = 1
    PREPHASE = 2
    BATTLEPHASE = 3
    POSTPHASE = 4
    _MAX = 5


# DIRECTIONS = {
#     0:"NE",
#     (-1,0): "NE",
#     1:"SE",
#     (0,1): "SE",
#     2:"SW",
#     (1,0): "SW",
#     3:"NW",
#     (0,-1): "NW"
# }

RIVER = {
    (0,-1,1,0):0,
    (-1,0,0,1):0,
    (0,1,1,0):1,
    (-1,0,0,-1):1,
    (0,1,-1,0):2,
    (1,0,0,-1):2,
    (0,-1,-1,0):3,
    (1,0,0,1):3,
    (0,-1,0,-1):4,
    (0,1,0,1):4,
    (-1,0,-1,0):5,
    (-1,0,1,0):5,
    (1,0,1,0):5,
    (1,0,-1,0):5,
}

TILE_IDS = [
    None,
    "Dirt",
    "Water",
    "Lava",
    "Rock"
]

EFFECT_IDS = [
    None,
    "Base,",
    "Fire",
    "Mountain",
    "River",
    "Wheat",
    "Town",
    "Heal"
]

UNIT_IDS = [
    None,
    "Base",
    "Saucer", 
    "BloodWraith", 
    "Homebase", 
    "Knight", 
    "Burrower",
    "SirenHead"
]
