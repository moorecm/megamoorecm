import pygame

import player
import level


class Engine:
    def __init__(self):
        pygame.init()
        # screen buffer
        self.screen = pygame.display.set_mode((320, 240), flags=pygame.SCALED)
        # transparent overlay for debugging
        self.overlay = self.screen.copy()
        self.overlay.set_alpha(0)
        self.overlay.set_colorkey((0, 0, 0))

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
            if event.type == pygame.QUIT:
                self.done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.done = True
                elif event.key == pygame.K_d:  # d to show debugging overlay
                    if self.overlay.get_alpha() == 0:
                        self.overlay.set_alpha(127)
                    else:
                        self.overlay.set_alpha(0)

        self.players.update(dt=dt, events=events)

        collisions = pygame.sprite.groupcollide(
            self.players, self.foreground, False, False
        )
        for player, collided_with in collisions.items():
            for other in collided_with:
                # highlight blocks in yellow
                s = pygame.Surface((other.rect.width, other.rect.height))
                s.fill((255, 255, 0))
                self.overlay.blit(s, (other.rect.x, other.rect.y))
                # inform the player
                player.collision(dt, other)
            # highlight player adjusted position in green
            s = pygame.Surface((player.rect.width, player.rect.height))
            s.fill((0, 127, 0))
            self.overlay.blit(s, (player.rect.x, player.rect.y))

    def draw(self):
        self.level.draw(self.screen)
        self.screen.blit(self.overlay, (0, 0))
        self.players.draw(self.screen)

        pygame.display.flip()

        # reset buffers
        self.screen.fill((0, 0, 0))
        self.overlay.fill((0, 0, 0))

    def loop(self):
        self.done = False
        while not self.done:
            dt = self.clock.tick(self.fps)
            self.update(dt=dt)
            self.draw()
