import pygame.gfxdraw
import random
import numpy as np



def main():

    w = 500
    h = 500

    pygame.init()
    display = pygame.display.set_mode((350, 350))
    x = np.arange(0, w)
    y = np.arange(0, h)
    X, Y = np.meshgrid(x, y)
    Z = X + Y



    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        for y in range(h):
            for x in range(w):
                r = random.randint(0, 1)
                Z[y][x] = r * 255

        surf = pygame.surfarray.make_surface(Z)
        display.blit(surf, (0, 0))
        pygame.display.update()
    pygame.quit()

main()