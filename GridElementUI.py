import pygame.sprite

class GridElementUI(pygame.sprite.Sprite):
    def __init__(self, width:int=64, height:int=64):  
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.surface.Surface((width, height), pygame.SRCALPHA)
        self.image.fill((150,80,80))
        self.rect = self.image.get_rect()
        self.width = width
        self.height = height
        self.visible = True
        self.needsredraw = True