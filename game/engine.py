import pygame

import player
import level


class Engine:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((320, 240), flags=pygame.SCALED)
        self.clock = pygame.time.Clock()
        self.fps = 60

        self.foreground = pygame.sprite.Group()
        self.level = level.Level1(group=self.foreground)

        self.players = pygame.sprite.Group()
        self.player = player.Player()
        self.player.rect.clamp_ip(self.screen.get_rect())  # screen boundary
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

        collisions = pygame.sprite.groupcollide(
            self.players, self.foreground, False, False
        )
        for sprite, collided_with in collisions.items():
            for other in collided_with:
                sprite.collision(dt, other)

    def draw(self):
        self.screen.fill((0, 0, 0))

        self.level.draw(self.screen)
        self.players.draw(self.screen)

        pygame.display.flip()

    def loop(self):
        self.done = False
        while not self.done:
            dt = self.clock.tick(self.fps)
            self.update(dt=dt)
            self.draw()
