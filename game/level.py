import os

import pygame
import pytmx

import mapset


class Level1:
    def __init__(self, group):
        self.group = group
        self.map = pytmx.util_pygame.load_pygame("game/level1.tmx")
        for n, layer in enumerate(self.map.layers):
            for x, y, tile in layer.tiles():
                properties = self.map.get_tile_properties(x, y, n)
                if properties is not None:
                    width = properties.get("width")
                    height = properties.get("height")
                    if properties.get("type") == "solid":
                        self.group.add(
                            mapset.Solid(
                                image=tile,
                                rect=pygame.Rect(x * 16, y * 16, width, height),
                            )
                        )

    def draw(self, surface):
        for n, layer in enumerate(self.map.layers):
            for x, y, tile in layer.tiles():
                properties = self.map.get_tile_properties(x, y, n)
                if properties is not None:
                    width = properties.get("width")
                    height = properties.get("height")
                    surface.blit(tile, (x * width, y * height))
