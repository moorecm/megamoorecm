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
        self.images = []
        for pose in self.spritemodel:
            self.images.append(
                self.spritesheet.subsurface(
                    pygame.Rect(
                        self.spritemodel[pose]["x"],
                        self.spritemodel[pose]["y"],
                        self.spritemodel[pose]["w"],
                        self.spritemodel[pose]["h"],
                    )
                )
            )

        self.frame = 0
        self.image = self.images[self.frame]
        self.flip = False

        # starting position
        self.rect = pygame.Rect(160 - 16, 100 - 16, 32, 32)

        # blink animation
        self.blink_interval = 4000
        self.blink_duration = 180
        self._reset_blink_timer(last_blink=-2000)  # make the first blink sooner

    def _reset_blink_timer(self, last_blink=None):
        self.last_blink = (
            last_blink if last_blink is not None else pygame.time.get_ticks()
        )

    def _player_moved(self):
        self._reset_blink_timer()

    def handle(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                self.flip = False
                self._player_moved()
            elif event.key == pygame.K_LEFT:
                self.flip = True
                self._player_moved()

    def update(self):
        now = pygame.time.get_ticks()

        # blink periodically
        if now - self.last_blink > self.blink_interval:
            self.frame = 1
            if now - self.last_blink > self.blink_interval + self.blink_duration:
                self._reset_blink_timer()
        else:
            self.frame = 0
        self.image = self.images[self.frame]

        if self.flip:
            self.image = pygame.transform.flip(self.image, flip_x=True, flip_y=False)
