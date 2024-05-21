import pygame as pyg

class Button:
    def __init__(self, world, position, pressed):
        self.x, self.y = position
        self.width, self.height = 20, 2
        self.world = world
        
        self.pressed = pressed

        self.assets = self.world.assets["button"]

    def rect(self):
        return pyg.Rect(self.x, self.y, self.width, self.height)
    
    def render(self, surface: pyg.Surface):
        surface.blit(self.assets[self.pressed], (self.x, self.y))