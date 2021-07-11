PHASES = {
    0:("Pregamephase", 20),
    1:("Planningphase",10),
    2:("Prephase",      0),
    3:("Battlephase",   0),
    4:("Postphase",     0)
}

PREVIEWS = {
    0:"SelectionPreview.png",
    1:"MovementPreview.png",
    2:"TargetMovementPreview.png",
    3:"MovementPreviewArrowNE.png",
    (-1,0):"MovementPreviewArrowNE.png",
    #Straight1: NE <-> SW
    (-1,0,-1,0):"MovementPreviewStraight1.png",
    (-1,0,1,0):"MovementPreviewStraight1.png",
    (1,0,1,0):"MovementPreviewStraight1.png",
    (1,0,-1,0):"MovementPreviewStraight1.png",
    4:"MovementPreviewArrowSE.png",
    (0,1):"MovementPreviewArrowSE.png",
    #Straight2: NW <-> SE
    (0,-1,0,1):"MovementPreviewStraight2.png",
    (0,-1,0,-1):"MovementPreviewStraight2.png",
    (0,1,0,1):"MovementPreviewStraight2.png",
    (0,1,0,-1):"MovementPreviewStraight2.png",
    5:"MovementPreviewArrowSW.png",
    (1,0):"MovementPreviewArrowSW.png",
    6:"MovementPreviewArrowNW.png",
    (0,-1):"MovementPreviewArrowNW.png",

    (-1,0,0,1):"MovementPreviewBendN.png",
    (0,-1,1,0):"MovementPreviewBendN.png",
    (1,0,0,-1):"MovementPreviewBendS.png",
    (0,1,-1,0):"MovementPreviewBendS.png",
    (0,1,1,0):"MovementPreviewBendE.png",
    (-1,0,0,-1):"MovementPreviewBendE.png",
    (0,-1,-1,0):"MovementPreviewBendW.png",
    (1,0,0,1):"MovementPreviewBendW.png",
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
