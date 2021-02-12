import pygame
import random
import Utils
import math


class Tile:
    tiles = {
        0: 'grass',
        1: 'beach'
    }

    def __init__(self, Client, _type, pos):
        self.type = _type
        self.variant = 0
        self.Client = Client
        self.Pos = pygame.math.Vector2(pos)

        if self.type == 0:
            self.variant = random.randint(0, 5)

    def postInit(self):
        self.Level = self.Client.Level
        self.Frame = self.Client.Frame

    def render(self):
        img = pygame.transform.scale(Utils.Img(
            self.tiles[self.type] + str(self.variant)), (int(self.Frame.Zoom), int(self.Frame.Zoom)))

        rect = self.Client.screen.blit(img, self.Frame.toPixel(self.Pos))
