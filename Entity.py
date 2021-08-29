import pygame


class Entity:
    def __init__(self, client, init):
        self.Pos = pygame.math.Vector2(init.get("pos"))
        self.Velocity = pygame.math.Vector2(0, 0)
        self.Client = client


class Player(Entity):
    accel_max = 0.1
    speed_max = 0.5
    friction = 0.9

    def simulate(self, move):
        accel = pygame.math.Vector2(
            (-1 if move.get("a") else 0) +
            (1 if move.get("d") else 0),
            (-1 if move.get("w") else 0) +
            (1 if move.get("s") else 0)
        )

        if accel.x != 0 or accel.y != 0:
            accel = accel.normalize()

            accel.x *= self.accel_max
            accel.y *= self.accel_max

            self.Velocity.x += accel.x
            self.Velocity.y += accel.y

        new_speed = self.Velocity.length()

        if new_speed > self.speed_max:
            new_speed = self.speed_max

        if accel.x == 0 and accel.y == 0:
            new_speed *= self.friction

        self.Velocity.x = round(self.Velocity.x, 2)
        self.Velocity.y = round(self.Velocity.y, 2)

        if not round(self.Velocity.length(), 2) == 0:
            self.Velocity.scale_to_length(new_speed)
            self.Pos.x += self.Velocity.x * self.Client.time
            self.Pos.y += self.Velocity.y * self.Client.time

        self.Client.Frame.Pos.x = self.Pos.x
        self.Client.Frame.Pos.y = self.Pos.y
