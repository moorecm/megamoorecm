import pygame

import json


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # load the spritesheet
        self.spritesheet = pygame.image.load(
            "external/8bitmegaman/file/8bitmegaman.png"
        ).convert()
        # load the spritesheet metadata
        with open("game/8bitmegaman.json") as f:
            self.spritemodel = json.load(f)

        # prepare images
        self.images = {}
        for pose in self.spritemodel:
            self.images[pose] = self.spritesheet.subsurface(
                pygame.Rect(
                    self.spritemodel[pose]["x"],
                    self.spritemodel[pose]["y"],
                    self.spritemodel[pose]["w"],
                    self.spritemodel[pose]["h"],
                )
            )

        self.frame = "ready"
        self.image = self.images[self.frame]
        self.flip = False

        # initial speed and position
        self.x_speed = 0
        self.y_speed = 0
        self.rect = pygame.Rect(160 - 16, 100 - 16, 32, 32)

        # blink animation
        self.blink_interval_ms = 4000
        self.blink_duration_ms = 180
        self._reset_idle_timer(idle_ms=-2000)  # make the first blink sooner
        # running animation
        self.running_since = 0

    def _reset_idle_timer(self, idle_ms=None):
        self.idle_since = idle_ms if idle_ms is not None else pygame.time.get_ticks()

    def _move(self, x=0, y=0):
        if self.x_speed == 0 and x != 0:
            self.running_since = pygame.time.get_ticks()
        self.x_speed += x
        if self.x_speed < 0:
            self.flip = True
        elif self.x_speed > 0:
            self.flip = False
        self.y_speed += y
        self._reset_idle_timer()

    def handle(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                self._move(x=1)
            elif event.key == pygame.K_LEFT:
                self._move(x=-1)
            elif event.key == pygame.K_UP:
                self._move()

    def update(self):
        now = pygame.time.get_ticks()

        if self.x_speed != 0 or self.y_speed != 0:  # in motion
            # move sprite
            self.rect.x += self.x_speed
            self.rect.y += self.y_speed
            # animate
            n = int((now - self.running_since) / 100) % 4
            print(n)
            if n == 0:
                self.frame = "run1"
            elif n == 1 or n == 3:
                self.frame = "run2"
            elif n == 2:
                self.frame = "run3"
        elif self.x_speed == 0 and self.y_speed == 0:  # stopped
            self.frame = "ready"

        if now - self.idle_since > self.blink_interval_ms:  # idle
            # blink periodically
            self.frame = "blink"
            if now - self.idle_since > self.blink_interval_ms + self.blink_duration_ms:
                self._reset_idle_timer()
                self.frame = "ready"

        self.image = self.images[self.frame]

        if self.flip:
            self.image = pygame.transform.flip(self.image, flip_x=True, flip_y=False)
