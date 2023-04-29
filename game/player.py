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

        # initial position
        self.spawn(160 - 12, 100 - 16)

        # initial state
        self.set_state("idle", since_ms=-2000)  # make the first blink sooner

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.apply_force(x=1)
                elif event.key == pygame.K_LEFT:
                    self.apply_force(x=-1)
                elif event.key == pygame.K_UP:
                    pass

    def spawn(self, x, y):
        self.x_speed = 0
        self.y_speed = 0
        self.rect = pygame.Rect(x, y, 32, 32)

    def set_state(self, state, since_ms=None):
        self.state = state
        self.since = since_ms if since_ms is not None else pygame.time.get_ticks()

    def apply_force(self, x=0, y=0):
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

    def update_position(self):
        # update x position
        self.rect.x += self.x_speed
        # check x boundaries
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.x > 320 - 24:
            self.rect.x = 320 - 24

        # update y position
        self.rect.y += self.y_speed
        # check y boundaries
        if self.rect.y < 0:
            self.rect.y = 0
        elif self.rect.y > 200 - 32:
            self.rect.y = 200 - 32

    def select_frame(self):
        now = pygame.time.get_ticks()
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

    def create_image(self):
        self.image = (
            pygame.transform.flip(self.images[self.frame], flip_x=True, flip_y=False)
            if self.flip
            else self.images[self.frame]
        )

    def update(self, events=()):
        self.handle_events(events)
        self.update_position()
        self.select_frame()
        self.create_image()
