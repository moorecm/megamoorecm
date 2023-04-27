import pygame


class Engine:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode([320, 200])

    def __del__(self):
        pygame.quit()

    def loop(self):
        done = False
        while not done:
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        done = True
                elif event.type == pygame.QUIT:
                    done = True
