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

        self.dx = 0.0
        self.dy = 0.0
        self.state = None
        self.frame = "ready"
        self.animation_counter = 0
        self.image = self.images[self.frame]
        self.flip = False

        # initial position
        self.spawn(160 - 12, 0)

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
            if self.state != "spawning" and self.state != "spawned":
                # only jump if player is grounded
                if self.y == 240 - 32:
                    self.set_state("jumping")
                    self.apply_force(y=-0.8)

    def spawn(self, x, y):
        self.set_state("spawning")
        self.apply_force(y=0.8)
        self.x = float(x)
        self.y = float(y)
        self.rect = pygame.Rect(x, y, 32, 32)

    def set_state(self, state):
        if self.state != state:
            self.state = state
            self.animation_counter = 0

    def apply_force(self, x=0, y=0):
        self.dx += x
        # limit running velocity
        if self.dx < -0.2:
            self.dx = -0.2
        elif self.dx > 0.2:
            self.dx = 0.2

        self.dy += y
        # limit gravity, but let spawning teleport go faster
        if self.state == "spawning":
            if self.dy > 0.8:
                self.dy = 0.8
        else:
            if self.dy > 0.2:
                self.dy = 0.2

    def update_position(self, dt):
        # update y position
        prev_y = self.y
        self.y = self.y + self.dy * dt
        # check y boundaries
        if self.y < 0:
            self.y = 0
        elif self.y > 240 - 32:
            self.y = 240 - 32
            if self.state == "spawning":
                self.set_state("spawned")
            elif self.state == "jumping":
                # landed from a jump/fall
                self.set_state("idle")  # overwritten below
        self.rect.y = int(self.y)

        # detect state changes
        if (
            self.state != "spawning"
            and self.state != "spawned"
            and self.state != "jumping"
        ):
            if prev_y != self.y:
                # started falling
                self.set_state("jumping")

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
        if (
            self.state != "spawning"
            and self.state != "spawned"
            and self.state != "jumping"
        ):
            if prev_x == self.x:
                # no movement
                self.set_state("idle")
            else:
                # running
                self.set_state("running")

    def world_physics(self):
        # friction
        if self.dx < 0:
            self.apply_force(x=0.1)
        elif self.dx > 0:
            self.apply_force(x=-0.1)
        # gravity
        self.apply_force(y=0.05)

    def select_frame(self, dt):
        # animate
        if self.state == "idle":
            # blink periodically
            self.animation_counter += dt
            ms_per_frame = 100  # blink lasts 1 frame x 100 ms
            number_of_frames = 50  # blink every 50 x 100 ms (every 5s)
            i = int(self.animation_counter // ms_per_frame) % number_of_frames
            if i == 16:
                self.frame = "blink"
            else:
                self.frame = "ready"
        elif self.state == "running":
            # run
            self.animation_counter += dt
            ms_per_frame = 100
            number_of_frames = 4
            i = int(self.animation_counter // ms_per_frame) % number_of_frames
            # alternate run1 -> run2 -> run3 -> run2 and repeat
            if i == 0:
                self.frame = "run1"
            elif i == 1 or i == 3:
                self.frame = "run2"
            elif i == 2:
                self.frame = "run3"
        elif self.state == "jumping":
            self.frame = "jump"
        elif self.state == "spawning":
            # spawn
            self.frame = "tele1"
        elif self.state == "spawned":
            # animate spawn landing
            self.animation_counter += dt
            ms_per_frame = 100
            number_of_frames = 4
            i = int(self.animation_counter // ms_per_frame) % number_of_frames
            if i == 0:
                self.frame = "tele3"
            elif i == 1:
                self.frame = "tele2"
            elif i == 2:
                self.frame = "tele1"
            elif i == 3:
                self.set_state("ready")

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
        self.select_frame(dt)
        self.create_image()
        self.world_physics()
