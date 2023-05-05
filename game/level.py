import os

import pygame
import pytmx

import mapset


class Level1:
    def __init__(self, group):
        self.group = group
        width = 16
        height = 16
        self.map = pytmx.util_pygame.load_pygame("game/level1.tmx")
        for n, layer in enumerate(self.map.layers):
            for x, y, tile in layer.tiles():
                # x, y are tile indicies, not coordinates
                properties = self.map.get_tile_properties(x, y, n)
                if properties is not None:
                    x_offset = properties.get("x")  # x offset into tileset image
                    y_offset = properties.get("y")  # y offset into tileset image
                    # properties.get("width") is the tileset image width
                    # properties.get("height") is the tileset image height

                    # pytmx ignores the .tmx attributes and loads the whole tileset
                    # image into tile, so this clips it for each single tile.
                    tile = tile.subsurface(
                        pygame.Rect(x_offset, y_offset, width, height)
                    )

                    # add "solid" sprites to the collision detection group
                    if properties.get("type") == "solid":
                        self.group.add(
                            mapset.Solid(
                                image=tile,
                                rect=pygame.Rect(x * width, y * height, width, height),
                            )
                        )

    def draw(self, surface):
        width = 16
        height = 16
        for n, layer in enumerate(self.map.layers):
            for x, y, tile in layer.tiles():
                properties = self.map.get_tile_properties(x, y, n)
                if properties is not None:
                    x_offset = properties.get("x")
                    y_offset = properties.get("y")
                    tile = tile.subsurface(
                        pygame.Rect(x_offset, y_offset, width, height)
                    )
                    surface.blit(
                        tile, pygame.Rect(x * width, y * height, width, height)
                    )
