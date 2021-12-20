STANDARD_TILE_SIZE = (64, 96)
STANDARD_UNIT_SIZE = (64, 64)

class HUD:
    IMAGE_BORDER_WIDTH = 2
    IMAGE_BORDER_COLOR = (100,100,100,255)
    LABEL_HEIGHT = 22
    ELEM_WIDTH = 200
    FONT_SIZE = 25

class FLAGS:
    REDRAW_TILES   = 0b001
    REDRAW_UNITS   = 0b010
    REDRAW_EFFECTS = 0b100

    MOVEMENT_DEFAULT  = 0b001
    MOVEMENT_WATER    = 0b010
    MOVEMENT_MOUNTAIN = 0b100
    
class PHASES:
    PREGAMEPHASE = 0
    PLANNINGPHASE = 1
    PREPHASE = 2
    BATTLEPHASE = 3
    POSTPHASE = 4