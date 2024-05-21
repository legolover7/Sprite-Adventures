import pygame as pyg
import os

from classes.globals import Globals

class WindowManager:
    def __init__(self):
        pyg.init()
        info_object = pyg.display.Info()
        self.screen_width, self.screen_height = info_object.current_w, info_object.current_h
        Globals.WINDOW_WIDTH = self.screen_width
        Globals.WINDOW_HEIGHT = self.screen_height
        self.windowed = False

        Globals.WINDOW = pyg.display.set_mode((self.screen_width, self.screen_height), pyg.FULLSCREEN)
        pyg.display.set_caption("Sprite Adventure")
        os.system("cls")

    def resize(self, dimensions):
        pyg.display.set_mode(dimensions)
        Globals.WINDOW_WIDTH, Globals.WINDOW_HEIGHT = dimensions

    def fullscreen(self):
        if self.windowed:
            pyg.display.set_mode((self.screen_width, self.screen_height), pyg.FULLSCREEN)
            Globals.WINDOW_WIDTH = self.screen_width
            Globals.WINDOW_HEIGHT = self.screen_height

        else:
            pyg.display.set_mode((1066, 600))
            Globals.WINDOW_WIDTH = 1066
            Globals.WINDOW_HEIGHT = 600
            

        self.windowed = not self.windowed

    def update(self):
        pyg.display.update()