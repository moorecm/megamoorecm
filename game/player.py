import pygame

import json


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.spritesheet = pygame.image.load(
            "external/8bitmegaman/file/8bitmegaman.png"
        ).convert()
        with open("game/8bitmegaman.json") as f:
            self.spritemodel = json.load(f)
        self.image = self.spritesheet.subsurface(
            pygame.Rect(
                self.spritemodel["ready"]["x"],
                self.spritemodel["ready"]["y"],
                self.spritemodel["ready"]["w"],
                self.spritemodel["ready"]["h"],
            )
        )
        self.rect = pygame.Rect(160 - 16, 100 - 16, 32, 32)
