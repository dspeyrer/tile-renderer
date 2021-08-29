import pygame
import Utils
import Level
import random
import math
import Viewport
import pygame.locals


class Client:
    KillProcess = False
    time = None

    def __init__(self, options):
        self.options = options
        self.screen = pygame.display.set_mode(
            options.get("resolution"), (pygame.FULLSCREEN if options.get("isFullscreen") == True else 0) | pygame.RESIZABLE)
        self.clock = pygame.time.Clock()
        self.framerate = self.options.get('framerate')
        pygame.display.set_caption('Python Technology Project')
        pygame.display.set_icon(Utils.Img('icon'))
        pygame.font.init()
        self.debugFont = pygame.font.SysFont("consolas", 12)

        self.debugQueue = []

        self.Frame = Viewport.Viewport(self, (0, 0), 64)

        self.Level = Level.Level(
            self, {
                "mapOld": [[random.randint(0, 1) for i in range(50)] for i in range(50)],
                "playerPos": (0, 0)
            })
        self.Level.postInit()
        self.Frame.render(self.Level)

        pygame.display.flip()

        while not self.KillProcess:
            self.main()

    def main(self):
        self.time = self.clock.tick(self.framerate) / (1000 / self.framerate)

        # PROCESS INPUT

        keypress = []

        zoom = 0

        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                self.KillProcess = True
            elif event.type == pygame.locals.KEYDOWN:
                keypress.append(event.unicode)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    zoom = 1
                if event.button == 5:
                    zoom = -1
            elif event.type == pygame.VIDEORESIZE:
                self.Frame.updateDimensions(event.size)

        keysdown = pygame.key.get_pressed()

        move = {
            "w": "w" in keypress or keysdown[pygame.K_w],
            "a": "a" in keypress or keysdown[pygame.K_a],
            "s": "s" in keypress or keysdown[pygame.K_s],
            "d": "d" in keypress or keysdown[pygame.K_d]
        }

        # RUN SIMULATION

        self.Level.Player.simulate(move)
        self.Frame.simulate(zoom)

        # RENDER

        self.Frame.render(self.Level)

        for i in range(len(self.debugQueue)):
            self.screen.blit(self.debugFont.render(
                self.debugQueue[i], True, (0, 0, 0)), (5, 5 + i * 15))

        self.debugQueue = []

        pygame.display.flip()
        self.debug(str(self.clock.get_fps()) + ' fps')

    def debug(self, text):
        self.debugQueue.append(text)
