import pygame
import pygame.sprite
import pygame.transform
import pygame.font
import pygame.image
from itblib.ui.TextureManager import Textures
from itblib.Enums import PHASES, PREVIEWS
from itblib.Globals import ClassMapping
from itblib.gridelements.UnitsUI import UnitBaseUI
from itblib.ui.GridUI import GridUI
from itblib.Game import Session
from itblib.gridelements.Units import UnitBase
from itblib.net.NetEvents import NetEvents

class Hud(pygame.sprite.Sprite):
    """The HUD is used to display most information, like HP, abilities, etc."""

    def __init__(self, width:int, height:int, gridui:GridUI, playerid:int, session:Session):
        super().__init__()
        self.image = pygame.Surface((width, height)).convert_alpha()
        self.background = pygame.Surface((gridui.width, gridui.height)).convert_alpha()
        self.rect = self.image.get_rect()
        self.selectedunitui:UnitBaseUI = None
        self.gridui = gridui
        self.font = pygame.font.SysFont('latinmodernmono', 15)
        self.cursorgridpos = (0,0)
        self.cursorscreenpos = (0,0)
        # display for unit's stats and icons/numbers of abilities
        self.tilefontdisplay = pygame.Surface((100,20))
        self.unitfontdisplay = pygame.Surface((96,20))
        self.unitimagedisplay = pygame.Surface((64,64))
        self.abilitiesdisplay = pygame.Surface((96,20))
        self.abilitiesnumbers = pygame.Surface((96,20)).convert_alpha()
        self.timerdisplay = pygame.Surface((96,20)).convert_alpha()
        self.hitpoint = pygame.Surface((16,16))
        self.hitpoint.fill((0,200,0,255))
        self.hitpointdisplay = pygame.Surface((20,20))
        self.hitpointdisplay.fill((0,0,0,255))
        # colorful display of ability phasees
        self.phasemarkersdisplay = pygame.Surface((96,20))
        self.phasemarkers = []
        self.playerid = playerid
        self.session = session
        self.backgrounds = []
        for bgname in Textures.backgroundtexturemapping.values():
            img = pygame.image.load(Textures.texturepath + bgname).convert_alpha()
            scaledimg = pygame.Surface(self.image.get_size()).convert_alpha()
            pygame.transform.scale(img, self.image.get_size(), scaledimg)
            self.backgrounds.append(scaledimg)
        for color in ((75,75,55,255), (50,255,50,255), (255,50,50,255), (255,200,0,255)):
            marker = pygame.Surface((16,20))
            marker.fill(color)
            self.phasemarkers.append(marker)
    
    def escape_pressed(self):
        """Tell the server that the player wants to leave."""
        NetEvents.snd_netplayerleave(self.session._players[self.playerid])

    def unitselect(self, position:"tuple[int,int]"):
        """Mark a unit as selected, displaying it's stats in greater detail and allowing ability use."""
        unitui = self.gridui.get_unitui(position)
        if unitui != self.selectedunitui:
            if self.selectedunitui and self.selectedunitui._parentelement:
                self.selectedunitui._parentelement.trigger_hook("OnDeselectUnit")
        if unitui and unitui._parentelement:
            if unitui._parentelement.ownerid == self.playerid:
                self.selectedunitui = unitui
                unitui._parentelement.trigger_hook("OnSelect")
            else:
                print(self.playerid, unitui._parentelement.ownerid)
        else:
            self.selectedunitui = None
        self.redraw()
    
    def targetselect(self, position:"tuple[int,int]"):
        """Forward the position of the selected target to the selected unit's hooks or spawn a unit."""
        if self.gridui.grid.phase == 0 and \
        len(self.session._players[self.playerid]._initialunitids) > 0 and\
        self.gridui.grid.is_space_empty(False, position):
            id = self.session._players[self.playerid]._initialunitids.pop(0)
            self.gridui.grid.request_add_unit(*position, id, self.playerid)
        elif self.selectedunitui:
            self.selectedunitui._parentelement.trigger_hook("TargetSelected", [position])
        self.redraw()

    def activate_ability(self, slot:int):
        """Activate the ability with the according number, and deselect all others."""
        if self.selectedunitui and self.selectedunitui._parentelement:
            self.selectedunitui._parentelement.trigger_hook("OnDeselectAbilities")
            self.selectedunitui._parentelement.trigger_hook("UserAction" + str(slot))
            self.redraw()

    def display_unit(self, pos:"tuple[int,int]"):
        """Display the portrait, stats and other info of a unit."""
        self.unitfontdisplay.fill((60,60,60,255))
        self.abilitiesdisplay.fill((60,60,60,255))
        self.unitimagedisplay.fill((100,0,0,0))
        self.abilitiesnumbers.fill((0,0,0,0))
        self.phasemarkersdisplay.fill((0,0,0,0))
        unitui = self.gridui.uiunits[self.gridui.grid.c_to_i(pos)]
        if not unitui._parentelement and self.selectedunitui:
            unitui = self.selectedunitui
        if unitui.visible:
            self.unitimagedisplay.blit(unitui.image, (0,16), (0,0,64,64))
            self.unitfontdisplay.blit(
                self.font.render(
                    type(unitui._parentelement).__name__, True, (255,255,255,255)
                ), 
                (0,0)
            )
            self.display_abilities(unitui._parentelement)
            self.display_healthbar(unitui._parentelement)
        self.image.blit(self.unitimagedisplay, (self.gridui.width*.75, self.gridui.height*.03))
        self.image.blit(self.unitfontdisplay, (self.gridui.width*.855, self.gridui.height*.03))
        self.image.blit(self.abilitiesdisplay, (self.gridui.width*.855, self.gridui.height*.1))
        self.image.blit(self.phasemarkersdisplay, (self.gridui.width*.855,self.gridui.height*.1+18))
        self.image.blit(self.abilitiesnumbers, (self.gridui.width*.855+5, self.gridui.height*.1+18))

    def display_abilities(self, unit:UnitBase):
        """Display the ability of a unit."""
        abilities = unit.abilities.values()
        index = 0
        numbers = ""
        for ability in abilities:
            if ability.id in Textures.abilitytexturemapping.keys():
                abilityimage = pygame.image.load(
                    Textures.texturepath+Textures.abilitytexturemapping[ability.id])
                self.abilitiesdisplay.blit(abilityimage, (16*index, 2), (0,0,16,16))
                self.phasemarkersdisplay.blit(self.phasemarkers[ability.phase], 
                    (16*index, 0))
                numbers += str(index+1) + " "
                index += 1
            if self.selectedunitui and unit == self.selectedunitui._parentelement:
                numberimage = self.font.render(numbers.strip(), True, (255,255,255,255))
                self.abilitiesnumbers.blit(numberimage, (0,0))

    def display_healthbar(self, unit:UnitBase):
        """Display the health bar on top of a unit."""
        x,y = self.gridui.transform_grid_screen(unit.pos)
        barwidth = 32
        hitpoints = unit.hitpoints
        slotwidth = min(10, max(4, barwidth/hitpoints))
        for hp in range(hitpoints):
            self.image.blit(self.hitpointdisplay,
                (x+32+slotwidth*hp-slotwidth/2*hitpoints,y-16),
                (0,0,slotwidth+2,8))
            self.image.blit(self.hitpoint, 
                (x+33+slotwidth*hp-slotwidth/2*hitpoints,y-15), 
                (0,0,slotwidth,6))
    
    def display_effect(self, pos:"tuple[int,int]"):
        """Display the effect the cursor is on."""
        effect = self.gridui.uieffects[self.gridui.grid.c_to_i(pos)]
        if effect.visible:
            self.image.blit(effect.image, (self.gridui.width*.75, self.gridui.height*.75), (0,0,64,64))

    def display_tile(self, pos:"tuple[int,int]"):
        """Display the tile the cursor is on."""
        self.tilefontdisplay.fill((0,0,0,0))
        tile = self.gridui.uitiles[self.gridui.grid.c_to_i(pos)]
        effect = self.gridui.uieffects[self.gridui.grid.c_to_i(pos)]
        if tile.visible:
            self.tilefontdisplay.blit(
                self.font.render(type(tile._parentelement).__name__, 
                True, 
                (255,255,255,255)), 
                (0,0)
            )
            self.image.blit(tile.image, (self.gridui.width*.75, self.gridui.height*.75), (0,0,64,64))
        self.image.blit(self.tilefontdisplay, (self.gridui.width*.85, self.gridui.height*.7))

    def redraw(self):
        """Update the internal image, so that no residual blits are seen."""
        self.background.blit(self.backgrounds[self.gridui.grid.phase], (0,0))
        self.image.fill((0,0,0,0))
        if self.selectedunitui and self.selectedunitui._parentelement:
            for ability in self.selectedunitui._parentelement.abilities.values():
                for previewinfo in ability.area_of_effect:
                    pos, previewid = previewinfo
                    screenpos = self.gridui.transform_grid_screen(pos)
                    self.image.blit(Textures.get_spritesheet(previewid)[0], screenpos)
        if self.selectedunitui and\
        self.selectedunitui._parentelement and\
        "MovementAbility" in self.selectedunitui._parentelement.abilities.keys() and\
        self.cursorgridpos in self.selectedunitui._parentelement.abilities["MovementAbility"].area_of_effect:
            self.image.blit(Textures.get_spritesheet(PREVIEWS[2])[0], self.cursorscreenpos)
        else:
            self.image.blit(Textures.get_spritesheet(PREVIEWS[0])[0], self.cursorscreenpos)
        
        maxphasetime = PHASES[self.gridui.grid.phase][1]
        currentphasetime = self.gridui.grid.phasetime
        self.timerdisplay = self.font.render(str(round(maxphasetime-currentphasetime, 1)), True, (255,255,255,255))
        self.image.blit(self.timerdisplay, (10,10))

        self.display_tile(self.cursorgridpos)
        self.display_effect(self.cursorgridpos)
        self.display_unit(self.cursorgridpos)

    def update_cursor(self, position:"tuple[int,int]"):
        """Forward the new cursor position to a unit's according hooks"""
        self.cursorgridpos = position
        self.cursorscreenpos = self.gridui.transform_grid_screen(position)
        if self.selectedunitui and self.selectedunitui._parentelement:
            self.selectedunitui._parentelement.trigger_hook("OnUpdateCursor", position)
        self.redraw()
    