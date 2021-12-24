import pygame

from itblib.ui.PerfSprite import PerfSprite

class MultiSprite(PerfSprite):
    """This class can be used to create "animated" sprites, using either a given set of textures
    that will be flipped through or by overriding the update and start methods to create variable animations"""
    def __init__(self, textures:"list[pygame.Surface]", global_transform:"pygame.Rect", frametime:float=.5, playing=False, looping=True):
        super().__init__()
        self._textures = textures
        self.frametime = frametime
        self.framenumber = -1
        self.animtime = -1
        self.playing = playing
        self.looping = looping
        self.local_transform = (0,0,*(global_transform[2:]))
        self.global_transform = global_transform
        self.blits:"list[tuple[pygame.Surface, pygame.Rect, pygame.Rect]]" = []

    def update(self, delta_time:float):
        """Called every frame, advances one anim frame if the frametime is reached."""
        if not self.playing:
            return
        self.animtime += delta_time
        currentframe = int(self.animtime/self.frametime)
        if currentframe > self.framenumber:
            if currentframe >= len(self._textures):
                if self.looping:
                    self.set_frame(0)
                    self.animtime = 0
                else:
                    self.stop()
            else:
                self.set_frame(currentframe)

    def start(self):
        """Set this animation into a "playing" state, enabling the update method."""
        if not self.playing:
            self.playing = True
            self.animtime = 0

    def stop(self):
        """Stop the animation, disabling the update method"""
        if self.playing:
            self.playing = False
    
    def set_frame(self, framenumber:int):
        """Set the animation to a certain frame. When start() is called, play from there."""
        self.framenumber = framenumber
        self.blits = [(self._textures[self.framenumber], self.global_transform, self.local_transform)]
    
    def get_blits(self) -> "Generator[tuple[pygame.Surface, pygame.Rect, pygame.Rect]]":
        yield from self.blits

    def set_textures(self, textures:"list[pygame.Surface]"):
        self._textures = textures
        self.framenumber = 0
        self.animtime = 0
        self.set_frame(0)
    