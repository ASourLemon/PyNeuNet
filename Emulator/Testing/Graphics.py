import pygame.gfxdraw
import random



def main():

    w = 500
    h = 500

    pygame.init()
    pygame.display.gl_set_attribute(pygame.GL_ACCELERATED_VISUAL, 1)
    screen = pygame.display.set_mode((w,h))
    screen.fill((0, 0, 0))
    s = pygame.Surface(screen.get_size(), pygame.OPENGL, 32)

    frame = 0
    try:
        while 1:
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.unicode == 'q':
                    break

            for y in range(h):
                for x in range(w):
                    r = random.randint(0, 1)
                    pygame.gfxdraw.pixel(s, x, y, (r * 255, r * 255, r * 255))

            frame += 1
            screen.blit(s, (0, 0))
            pygame.display.update()
    finally:
        pygame.quit()

    print("Frames: " + str(frame))
    print("Done!")

main()