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
        self.state = None
        self.set_state("idle", -2000)  # make the first blink sooner

    def handle_events(self, events):
        # singular events (key up, key down, etc.)
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    pass
                elif event.key == pygame.K_LEFT:
                    pass
                elif event.key == pygame.K_UP:
                    pass
        # pressed keys
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.apply_force(x=-0.1)
        if keys[pygame.K_RIGHT]:
            self.apply_force(x=0.1)
        if keys[pygame.K_UP]:
            pass

    def spawn(self, x, y):
        self.dx = 0.0
        self.dy = 0.0
        self.x = float(x)
        self.y = float(y)
        self.rect = pygame.Rect(x, y, 32, 32)

    def set_state(self, state, since_ms=None):
        if self.state != state:
            self.state = state
            self.since = since_ms if since_ms is not None else pygame.time.get_ticks()

    def apply_force(self, x=0, y=0):
        self.dx += x
        if self.dx < -0.2:
            self.dx = -0.2
        elif self.dx > 0.2:
            self.dx = 0.2

        self.dy += y
        if self.dy < -0.2:
            self.dy = -0.2
        elif self.dy > 0.2:
            self.dy = 0.2

    def update_position(self, dt):
        # update x position
        prev_x = self.x
        self.x = self.x + self.dx * dt
        # check x boundaries
        if self.x < 0:
            self.x = 0
        elif self.x > 320 - 24:
            self.x = 320 - 24
        self.rect.x = int(self.x)

        # detect state changes
        if prev_x == self.x:
            # no movement
            self.set_state("idle")
        else:
            # running
            self.set_state("running")

        # update y position
        prev_y = self.y
        self.y = self.y + self.dy * dt
        # check y boundaries
        if self.y < 0:
            self.y = 0
        elif self.y > 200 - 32:
            self.y = 200 - 32
        self.rect.y = int(self.y)

    def world_physics(self):
        # friction
        if self.dx < 0:
            self.apply_force(x=0.1)
        elif self.dx > 0:
            self.apply_force(x=-0.1)
        # gravity
        # self.apply_force(y=0.2)

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
                    self.since = pygame.time.get_ticks()
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

        # facing left or right?
        if self.dx < 0:
            self.flip = True
        elif self.dx > 0:
            self.flip = False

    def create_image(self):
        self.image = (
            pygame.transform.flip(self.images[self.frame], flip_x=True, flip_y=False)
            if self.flip
            else self.images[self.frame]
        )

    def update(self, dt, events=()):
        self.handle_events(events)
        self.update_position(dt)
        self.select_frame()
        self.create_image()
        self.world_physics()
