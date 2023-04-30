import os

import pygame
import pytmx


class Level1:
    def __init__(self):
        self.map = pytmx.util_pygame.load_pygame("game/level1.tmx")

    def draw(self, surface):
        for n, layer in enumerate(self.map.layers):
            for x, y, tile in layer.tiles():
                properties = self.map.get_tile_properties(x, y, n)
                if properties is not None:
                    print(properties.get("type"))

                    width = properties.get("width")
                    height = properties.get("height")

                    surface.blit(tile, (x * width, y * height))
