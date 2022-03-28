"""Contains various animations."""

from typing import TYPE_CHECKING
from itblib.components import ComponentAcceptor, TransformComponent
from itblib.globals.Colors import BLACK, DARK_GRAY, LIGHT_GRAY
from itblib.ui.IGraphics import IGraphics
from itblib.ui.particles import TrailParticleSpawner
import pygame
from itblib.Vec import add, smult
if TYPE_CHECKING:
    from typing import Generator, Callable
    from itblib.Player import Player


class Animation(ComponentAcceptor, IGraphics):
    """
    The base class for other animations. Contains simple state management and time tracking.
    """
    def __init__(self) -> None:
        super().__init__()
        self.tfc = TransformComponent()
        self.tfc.attach_component(self)
        self._animation_time = 0
        self._running = False
    
    def start(self):
        """Start the animation."""
        self._running = True
    
    def stop(self):
        """Stop the animation."""
        self._running = False

    def tick(self, delta_time:float):
        """Tick the animation."""
        if self._running:
            self._animation_time += delta_time
            self._update(delta_time)
    
    def _update(self, delta_time:float):
        """Called after the tick method when the animation is running."""
    

class FlipbookAnimation(Animation):
    """
    This animation can be used to create flibook-like visuals,
    i.e. displaying each frame for a set duration.
    """
    def __init__(self, textures:"list[pygame.Surface]", frametime:float=.5, running=False, looping=True) -> None:
        super().__init__()
        self._frametime = frametime
        self._running = running
        self._looping = looping
        self._framenumber = -1
        self._textures = textures

    def start(self):
        super().start()
        self._animation_time = 0
    
    def get_blits(self) -> "Generator[tuple[pygame.Surface, pygame.Rect, pygame.Rect]]":
        texdim = self._textures[self._framenumber].get_size()
        yield ( self._textures[self._framenumber], 
            pygame.Rect(self.tfc.get_position(), texdim), 
            pygame.Rect(0,0,*texdim))
    
    def set_textures(self, textures:"list[pygame.Surface]"):
        self._textures = textures
        self._framenumber = 0
        self._animation_time = 0

    def _update(self, delta_time:float):
        super()._update(delta_time)
        currentframe = int(self._animation_time/self._frametime)
        if currentframe > self._framenumber:
            if currentframe >= len(self._textures):
                if self._looping:
                    self._framenumber = 0
                    self._animation_time = 0
                else:
                    self.stop()
            else:
                self._framenumber = currentframe
    

class ProjectileAnimation(Animation):
    def __init__(self, pos_func:"Callable[[float],tuple[int,int]]"):
        super().__init__()
        self._particles_spawner = TrailParticleSpawner()
        self._projectile_radius = 3
        self._projectile_size = (self._projectile_radius*2+1,self._projectile_radius*2+1)
        self._projectile_texture = pygame.Surface(self._projectile_size).convert_alpha()
        self._projectile_texture.fill((0))
        self._pos = (0,0)
        self._pos_func = pos_func
        pygame.draw.circle(
            self._projectile_texture,
            DARK_GRAY,
            (self._projectile_radius,self._projectile_radius),
            self._projectile_radius
        )
    
    def get_blits(self) -> "Generator[tuple[pygame.Surface, pygame.Rect, pygame.Rect]]":
        yield (self._projectile_texture, pygame.Rect(self._pos, self._projectile_size), self._projectile_texture.get_rect())
        yield from self._particles_spawner.get_blits()
    
    def _update(self, delta_time: float):
        self._animation_time += delta_time
        if self._running:
            self._pos = self._pos_func(self._animation_time)
            self._particles_spawner.position = add(self._pos, smult(.5, self._projectile_size))
            self._particles_spawner.update(delta_time)

class PlayerVersusAnimation(Animation):
    def __init__(self, player1:"Player", player2:"Player", width, height):
        super().__init__()
        self._font = pygame.font.Font('HighOne.ttf', 32)
        self._width = width
        self._height = height
        
        self._p1_surf = PlayerVersusAnimation._create_player_polygon(player1, False, self._font)
        self._p2_surf = PlayerVersusAnimation._create_player_polygon(player2, True , self._font)
        self._poly_size = self._p1_surf.get_size()
        
        self._bar_line_width = 2
        self._bar_width = self._width
        self._bar_height = self._poly_size[1] + 2 * self._bar_line_width
        self._bar_surf = pygame.Surface((self._bar_width, self._bar_height))
        self._clear_blit = pygame.Surface((self._bar_width, self._bar_height))
        self._clear_blit.fill(BLACK)
        bar_top_l = (0              , 0)
        bar_top_r = (self._bar_width, 0)
        bar_bot_l = (0              , self._bar_height - self._bar_line_width)
        bar_bot_r = (self._bar_width, self._bar_height - self._bar_line_width)
        pygame.draw.line(self._bar_surf, LIGHT_GRAY, bar_top_l, bar_top_r, self._bar_line_width)
        pygame.draw.line(self._bar_surf, LIGHT_GRAY, bar_bot_l, bar_bot_r, self._bar_line_width)
        
        self.retreating = False
        self._retreat_time = 2.5
        self._last_blit_time = 2.0
        self._running = True

    def get_blits(self) -> "Generator[tuple[pygame.Surface, pygame.Rect, pygame.Rect]]":
        p1_start_pos = (0,self._bar_line_width)
        p2_start_pos = (
            self._width  - self._p2_surf.get_width(),
            self._height - self._p2_surf.get_height() - self._bar_line_width
        )
        p1_delta_pos = (self._posfunc(), 0)
        p2_delta_pos = (-self._posfunc(), 0)
        p1_rect = pygame.Rect(add(p1_start_pos, p1_delta_pos), self._p1_surf.get_size())
        p2_rect = pygame.Rect(add(p2_start_pos, p2_delta_pos), self._p2_surf.get_size())
        if self._animation_time >= self._retreat_time:
            r1, r2 = self._get_bar_rects(self._last_blit_time)
            self._last_blit_time = self._animation_time
            yield from [
                (self._clear_blit, r1, self._bar_surf.get_rect()), 
                (self._clear_blit, r2, self._bar_surf.get_rect())
                ]
        r1, r2 = self._get_bar_rects(self._animation_time)
        yield from [
            (self._bar_surf, r1, self._bar_surf.get_rect()),
            (self._bar_surf, r2, self._bar_surf.get_rect())
            ]
        yield (self._p1_surf, p1_rect, pygame.Rect(0,0,*self._poly_size))
        yield (self._p2_surf, p2_rect, pygame.Rect(0,0,*self._poly_size))
        
    
    @staticmethod
    def _create_player_polygon(player:"Player", flip:bool, font:pygame.font.Font):
        x, y = size = (200, 50)
        polyanchors = [(0, 0), (x, 0), size, (30, y)]
        poly_surface = pygame.Surface(size).convert_alpha()
        poly_surface.fill((0))
        pygame.draw.polygon(poly_surface, player.color, polyanchors)
        name_text = font.render(player.name, True, (255))
        poly_surface.blit(name_text, (polyanchors[3][0]-5, polyanchors[0][1]+2))
        return poly_surface

    def _posfunc(self):
        """Resturns the x-position of the player's label at a certain time."""
        return (((self._animation_time-1)*7)**3)+((self._width-self._poly_size[0])/2)
    
    def _get_bar_rects(self, time:float) -> "tuple[pygame.Rect, pygame.Rect]":
        top_y = 0
        bot_y = self._height - self._poly_size[1] - 4
        if time >= self._retreat_time:
            m = min(max(time-self._retreat_time,0)*2,1)
            top_y += m * -(self._poly_size[1]+2)
            bot_y += m * (self._poly_size[1]+2)
        size = (self._width, self._poly_size[1]+4)
        top_rect = pygame.Rect((0, top_y), size)
        bot_rect = pygame.Rect((0, bot_y), size)
        return top_rect, bot_rect
