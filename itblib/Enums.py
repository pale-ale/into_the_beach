PHASES = {
    0:("Pregamephase", 20),
    1:("Planningphase",10),
    2:("Prephase",      0),
    3:("Battlephase",   0),
    4:("Postphase",     0)
}

PREVIEWS = {
    0:"SelectionPreview",
    1:"MovementPreview",
    2:"TargetMovementPreview",
    3:"MovementPreviewArrowNE",
    (-1,0):"MovementPreviewArrowNE",
    #Straight1: NE <-> SW
    (-1,0,-1,0):"MovementPreviewStraightNE",
    (-1,0,1,0):"MovementPreviewStraightNE",
    (1,0,1,0):"MovementPreviewStraightNE",
    (1,0,-1,0):"MovementPreviewStraightNE",
    4:"MovementPreviewArrowSE",
    (0,1):"MovementPreviewArrowSE",
    #Straight2: NW <-> SE
    (0,-1,0,1):"MovementPreviewStraightNW",
    (0,-1,0,-1):"MovementPreviewStraightNW",
    (0,1,0,1):"MovementPreviewStraightNW",
    (0,1,0,-1):"MovementPreviewStraightNW",
    5:"MovementPreviewArrowSW",
    (1,0):"MovementPreviewArrowSW",
    6:"MovementPreviewArrowNW",
    (0,-1):"MovementPreviewArrowNW",

    (-1,0,0,1):"MovementPreviewBendN",
    (0,-1,1,0):"MovementPreviewBendN",
    (1,0,0,-1):"MovementPreviewBendS",
    (0,1,-1,0):"MovementPreviewBendS",
    (0,1,1,0):"MovementPreviewBendE",
    (-1,0,0,-1):"MovementPreviewBendE",
    (0,-1,-1,0):"MovementPreviewBendW",
    (1,0,0,1):"MovementPreviewBendW",
}

DIRECTIONS = {
    0:"NE",
    (-1,0): "NE",
    1:"SE",
    (0,1): "SE",
    2:"SW",
    (1,0): "SW",
    3:"NW",
    (0,-1): "NW"
}

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
    (1,0,1,0):5,
}
