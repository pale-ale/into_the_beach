from itblib.globals.Enums import PHASES

STANDARD_TILE_SIZE = (64, 96)
STANDARD_UNIT_SIZE = (64, 64)

class HUD:
    IMAGE_BORDER_WIDTH = 2
    LABEL_HEIGHT = 22
    ELEM_WIDTH = 200
    TITLE_FONT_SIZE = 32
    DESC_FONT_SIZE = 16
    SMALL_FONT_SIZE = 12

class FLAGS:
    MOVEMENT_DEFAULT  = 0b001
    MOVEMENT_WATER    = 0b010
    MOVEMENT_MOUNTAIN = 0b100

class PHASE_DURATIONS:
    # Keys are itblib.globals.Enums.PHASES, values are durations in seconds 
    DURATIONS = {
        PHASES.PREGAMEPHASE :20,
        PHASES.PLANNINGPHASE:10,
        PHASES.PREPHASE     : 0,
        PHASES.BATTLEPHASE  : 0,
        PHASES.POSTPHASE    : 0
    }

class PHASE_NAMES:
    NAMES = {
        PHASES.PREGAMEPHASE :"Pregamephase" , 
        PHASES.PLANNINGPHASE:"Planningphase",
        PHASES.PREPHASE     :"Prephase"     ,     
        PHASES.BATTLEPHASE  :"Battlephase"  ,  
        PHASES.POSTPHASE    :"Postphase"
    }

