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

        # initial state
        self.set_state("idle", since_ms=-2000)  # make the first blink sooner

    def set_state(self, state, since_ms=None):
        self.state = state
        self.since = since_ms if since_ms is not None else pygame.time.get_ticks()

    def _move(self, x=0, y=0):
        self.x_speed += x

        # detect state changes
        if self.x_speed == 0 and x != 0:
            # just stopped
            self.set_state("idle")
        elif (self.x_speed < 0 and self.x_speed - x < 0) or (
            self.x_speed > 0 and self.x_speed - x > 0
        ):
            pass  # no state change
        else:
            # just started running
            self.set_state("running")

        # facing left or right?
        if self.x_speed < 0:
            self.flip = True
        elif self.x_speed > 0:
            self.flip = False

        self.y_speed += y

    def handle(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                self._move(x=1)
            elif event.key == pygame.K_LEFT:
                self._move(x=-1)
            elif event.key == pygame.K_UP:
                pass

    def update(self):
        now = pygame.time.get_ticks()

        # update position
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed

        # select frame
        if self.state == "idle":
            # blink periodically
            blink_interval_ms = 4000
            blink_duration_ms = 180
            if now - self.since > blink_interval_ms:
                self.frame = "blink"
                if now - self.since > blink_interval_ms + blink_duration_ms:
                    self.frame = "ready"
            else:
                self.frame = "ready"
        elif self.state == "running":
            # animate
            n = (now - self.since) // 100 % 4
            if n == 0:
                self.frame = "run1"
            elif n == 1 or n == 3:
                self.frame = "run2"
            elif n == 2:
                self.frame = "run3"

        self.image = self.images[self.frame]

        if self.flip:
            self.image = pygame.transform.flip(self.image, flip_x=True, flip_y=False)
