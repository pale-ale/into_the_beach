import pygame
import pygame.display
import pygame.time
import pygame.sprite
from math import pi

PIXELSIZE = 2

pygame.display.init()
i = pygame.display.Info()
ssize = (i.current_w, i.current_h)
size = (int(ssize[0]/PIXELSIZE), int(ssize[1]/PIXELSIZE))
screen = pygame.display.set_mode(ssize, pygame.NOFRAME)
image = pygame.Surface(size)

def get_parabola(point, peak):
    t_point = (point[0] - peak[0], point[1] - peak[1])
    a = t_point[1]/t_point[0]**2
    def parabola(x):
        nonlocal a
        return int(a * (x**2))
    return parabola


def draw_parabola(peak, p1, p2):
    for point in (p1,p2):
        p = get_parabola(point, peak)
        prev_point = (peak)
        for x in range(int(peak[0]), int(point[0]), 3 if peak[0] < point[0] else -3):
            next_point = (x, p(x-peak[0])+peak[1])
            print(next_point)
            pygame.draw.line(image, (255,255,0), prev_point, next_point, 2)
            prev_point = next_point

p_1 = (size[0]/2, size[1]/2)
p_2 = (size[0]-20, size[1]/2)
p_peak = ((p_1[0] + p_2[0]) / 2 - 50, max(p_1[1], p_1[1])+50)
pygame.draw.circle(image, (50,255,50), p_1, 10)
pygame.draw.circle(image, (50,50,255), p_2, 10)
pygame.draw.circle(image, (255,50,255), p_peak, 10)

def main():
    global p_peak
    RUNNING = True

    while RUNNING:
        image.fill(0)
        p_peak = (p_peak[0], p_peak[1]+1)
        draw_parabola(p_peak, p_1, p_2)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                RUNNING = False
        pygame.transform.scale(image, screen.get_size(), screen)
        pygame.display.update()
    pygame.quit()

if __name__ == '__main__':
    main()
