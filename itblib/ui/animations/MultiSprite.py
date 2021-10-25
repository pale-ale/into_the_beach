import pygame

class MultiSprite(pygame.sprite.Sprite):
    """This class can be used to create "animated" sprites, using either a given set of textures
    that will be flipped through or by overriding the update and start methods to create variable animations"""
    def __init__(self, textures:"list[pygame.Surface]", width:int=64, height:int=64, frametime:float=.5, playing=False, looping=True):
        super().__init__()
        self.image = pygame.Surface((width, height), pygame.SRCALPHA).convert_alpha()
        self.rect = self.image.get_rect()
        self._textures = textures
        self.frametime = frametime
        self.framenumber = 0
        self.animtime = -1
        self.playing = playing
        self.looping = looping

    def update(self, dt:float):
        """Called every frame, advances one anim frame if the frametime is reached."""
        if not self.playing:
            return
        self.animtime += dt
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
        if not self.playing and len(self._textures) > 0:
            self.playing = True
            self.animtime = 0

    def stop(self):
        """Stop the animation, disabling the update method"""
        if self.playing:
            self.playing = False
    
    def set_frame(self, framenumber:int):
        """Set the animation to a certain frame. When start() is called, play from there."""
        self.framenumber = framenumber
        self.image.fill(0)
        self.image.blit(self._textures[self.framenumber], (0,0))
