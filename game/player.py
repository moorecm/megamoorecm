import pygame

import json
import time


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

        self.rect = pygame.Rect(160 - 16, 100 - 16, 32, 32)

        self.time = time.time()

    def handle(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                self.flip = False
            elif event.key == pygame.K_LEFT:
                self.flip = True

    def update(self):
        # blink periodically
        per_second_interval = 8
        count = 24
        counter = int((time.time() - self.time) * per_second_interval % count)
        if counter == 8:
            self.frame = 1
        else:
            self.frame = 0
        self.image = self.images[self.frame]

        if self.flip:
            self.image = pygame.transform.flip(self.image, flip_x=True, flip_y=False)
