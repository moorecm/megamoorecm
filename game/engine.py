import pygame

import player


class Engine:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode([320, 200])
        self.clock = pygame.time.Clock()
        self.players = pygame.sprite.Group()
        self.player = player.Player()
        self.players.add(self.player)

    def __del__(self):
        pygame.quit()

    def loop(self):
        done = False
        while not done:
            #
            # handle events
            #
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        done = True
                elif event.type == pygame.QUIT:
                    done = True
            #
            # update state
            #
            self.players.update()
            #
            # render
            #
            self.players.draw(self.screen)
            pygame.display.flip()
            #
            # synchronize
            #
            self.clock.tick(30)
