import sys

print(f"Python {sys.version}")

import pygame


def main():
    pygame.init()
    screen = pygame.display.set_mode([320, 200])
    done = False
    while not done:
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True
            elif event.type == pygame.QUIT:
                done = True
    pygame.quit()


if __name__ == "__main__":
    sys.exit(main())
