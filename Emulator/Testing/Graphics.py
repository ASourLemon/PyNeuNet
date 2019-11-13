import pygame
import random

width = 250
height = 250

pygame.init()
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
running = True

x = 0
y = 0
frame = 0

while running:

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    r = random.randint(0, 1)
    screen.set_at((x, y), (r * 255, r * 255, r * 255))

    x += 1
    if x > width:
        x = 0
        y += 1
        if y > height:
            y = 0
            frame += 1
            screen.convert()
            pygame.display.update()
            pygame.display.set_caption("Frame: " + str(frame))

pygame.quit()
