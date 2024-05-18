import pygame as pyg

from scripts.entities import PhysicsEntity

class Coin(PhysicsEntity):
    def __init__(self, world, position):
        self.world = world
        self.x, self.y = position
        self.width, self.height = 20, 20
        self.animation = self.world.assets["coin"].copy()

    def render(self, surface: pyg.Surface):
        surface.blit(self.animation.image(), (self.x, self.y))

