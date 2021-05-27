import pygame

WIDTH = 1000
HEIGHT = 700
BLACK = [0, 0, 0] 
GREEN = [0, 255, 0]
RED = [255, 0, 0]
pygame.init()
pygame.mixer.init()
pygame.display.set_caption("<GeoDash>")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
world = pygame.surface.Surface((WIDTH,HEIGHT))
RUNNING = True

sprites = pygame.sprite.Group()

while RUNNING:
    world.fill((0,0,0))
    sprites.draw(world)
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            RUNNING = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                RUNNING = False
    pygame.display.flip()
pygame.quit()
