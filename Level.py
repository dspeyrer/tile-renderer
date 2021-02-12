import Tile
import Entity


class Level:
    def __init__(self, Client, lvl):
        self.Level = lvl
        self.Map = self.Level.get("mapOld")
        self.Client = Client
        self.Player = Entity.Player(self.Client, {
            "pos": self.Level.get("playerPos")
        })

        for y in range(len(self.Map)):
            for x in range(len(self.Map[y])):
                self.Map[y][x] = Tile.Tile(
                    self.Client, self.Map[y][x], (x, y))

    def postInit(self):
        for i in self.Map:
            for j in i:
                j.postInit()
