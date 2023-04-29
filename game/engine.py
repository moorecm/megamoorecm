import pygame

import player


class Engine:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((320, 200), flags=pygame.SCALED)
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.players = pygame.sprite.Group()
        self.player = player.Player()
        self.players.add(self.player)

    def __del__(self):
        pygame.quit()

    def update(self, dt, events=None):
        pygame.display.set_caption(f"{self.clock.get_fps():.1f} FPS")

        if events is None:
            events = pygame.event.get()

        for event in events:
            if (
                event.type == pygame.QUIT
                or event.type == pygame.KEYDOWN
                and event.key == pygame.K_ESCAPE
            ):
                self.done = True

        self.players.update(dt=dt, events=events)

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.players.draw(self.screen)

        pygame.display.flip()

    def loop(self):
        self.done = False
        while not self.done:
            dt = self.clock.tick(self.fps)
            self.update(dt=dt)
            self.draw()
