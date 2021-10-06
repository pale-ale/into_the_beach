import pygame

class MultiSprite(pygame.sprite.Sprite):
    def __init__(self, textures:"list[pygame.Surface]", width:int=64, height:int=64, frametime:float=.5):
        super().__init__()
        self.image = pygame.Surface((width, height), pygame.SRCALPHA).convert_alpha()
        self.rect = self.image.get_rect()
        self._textures = textures
        self.frametime = frametime
        self.framenumber = 0
        self.timestamp = -1
        self.playing = False
        self.set_frame(0)

    def update(self, dt:float):
        if not self.playing:
            return
        self.timestamp += dt
        currentframe = int(self.timestamp/self.frametime)
        if currentframe > self.framenumber:
            if currentframe >= len(self._textures):
                self.stop()
            else:
                self.framenumber = currentframe
                self.image.blit(self._textures[self.framenumber])

    def start(self):
        if not self.playing:
            self.playing = True
            self.timestamp = 0

    def stop(self):
        if self.playing:
            self.playing = False
    
    def set_frame(self, framenumber:int):
        self.image.blit(self._textures[self.framenumber], (0,0))
