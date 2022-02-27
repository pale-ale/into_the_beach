from typing import Generator

import pygame
from itblib.components.ComponentAcceptor import ComponentAcceptor
from itblib.components.TransformComponent import TransformComponent
from itblib.ui.IGraphics import IGraphics


class MultiSprite(ComponentAcceptor, IGraphics):
    """This class can be used to create "animated" sprites, using either a given set of textures
    that will be flipped through or by overriding the update and start methods to create variable animations"""
    def __init__(self, textures:"list[pygame.Surface]", frametime:float=.5, playing=False, looping=True):
        super().__init__()
        assert isinstance(frametime, float)
        self._textures = textures
        self.frametime = frametime
        self.framenumber = -1
        self.animtime = -1
        self.playing = playing
        self.looping = looping
        self.blits:"list[tuple[pygame.Surface, pygame.Rect, pygame.Rect]]" = []
        self.tfc = TransformComponent()
        self.tfc.attach_component(self)

    def update(self, delta_time:float):
        """Called every frame, advances one anim frame if the frametime is reached."""
        if not self.playing:
            return
        self.animtime += delta_time
        currentframe = int(self.animtime/self.frametime)
        if currentframe > self.framenumber:
            if currentframe >= len(self._textures):
                if self.looping:
                    self.framenumber = 0
                    self.animtime = 0
                else:
                    self.stop()
            else:
                self.framenumber = currentframe

    def start(self):
        """Set this animation into a "playing" state, enabling the update method."""
        if not self.playing:
            self.playing = True
            self.animtime = 0

    def stop(self):
        """Stop the animation, disabling the update method"""
        if self.playing:
            self.playing = False
    
    def get_blits(self) -> "Generator[tuple[pygame.Surface, pygame.Rect, pygame.Rect]]":
        texdim = self._textures[self.framenumber].get_size()
        yield ( self._textures[self.framenumber], 
            pygame.Rect(self.tfc.get_position(), texdim), 
            pygame.Rect(0,0,*texdim))

    def set_textures(self, textures:"list[pygame.Surface]"):
        self._textures = textures
        self.framenumber = 0
        self.animtime = 0
    