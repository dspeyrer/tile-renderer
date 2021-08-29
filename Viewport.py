import pygame
import math


class Viewport:
    zoom_speed = 2
    zoom_friction = 0.8
    zoom_max = 64
    zoom_min = 5

    def __init__(self, Client, pos, zoom):
        self.Pos = pygame.math.Vector2(pos)
        self.Client = Client
        self.Zoom = zoom
        self.Size = pygame.math.Vector2(
            pygame.display.get_surface().get_size())
        self.ZoomVel = 0

    def render(self, Level):
        self.Client.screen.fill((255, 255, 255))

        relativeSize = [
            math.ceil(self.Size.x / self.Zoom), math.ceil(self.Size.y / self.Zoom)]

        relativePos = [math.floor(
            self.Pos.x - relativeSize[0] / 2), math.floor(self.Pos.y - relativeSize[1] / 2)]


        if relativePos[0] < -relativeSize[0] or relativePos[1] < -relativeSize[1]:
            relativeSize = [0, 0]

        if relativePos[1] + relativeSize[1] > len(Level.Map):
            relativeSize[1] = len(Level.Map) - relativePos[1]
        if relativePos[0] + relativeSize[0] > len(Level.Map[0]):
            relativeSize[0] = len(Level.Map[0]) - relativePos[0]

        counter = 0

        for i in range(max(0, relativePos[1]), min(len(Level.Map), relativePos[1] + relativeSize[1] + 1)):
            for j in range(max(0, relativePos[0]), min(len(Level.Map[i]), relativePos[0] + relativeSize[0] + 1)):
                Level.Map[i][j].render()
                counter += 1

        self.Client.debug('Rendering ' + str(counter) + ' Tiles')

    def toPixel(self, pos):
        pixel = pos - self.Pos
        pixel *= int(self.Zoom)
        pixel.x += self.Size.x / 2
        pixel.y += self.Size.y / 2
        return pixel

    def simulate(self, zoom):
        self.ZoomVel += zoom * self.zoom_speed

        if zoom == 0:
            self.ZoomVel *= self.zoom_friction
            self.ZoomVel = math.trunc(self.ZoomVel * 1000) / 1000

        self.Zoom += self.ZoomVel * self.Client.time

        if self.Zoom < self.zoom_min:
          self.Zoom = self.zoom_min
          self.ZoomVel = 0

        if self.Zoom > self.zoom_max:
          self.Zoom = self.zoom_max
          self.ZoomVel = 0

        self.Client.debug("zoom velocity: " + str(self.ZoomVel))

    def updateDimensions(self, size):
        self.Size = pygame.math.Vector2(size)
        pygame.display.set_mode(
            size, (pygame.FULLSCREEN if self.Client.options.get("isFullscreen") == True else 0) + pygame.RESIZABLE)
