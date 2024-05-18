# Import statements
import pygame as pyg

# Classes
from classes.buttons import MenuButton
from classes.display import Colors, Fonts
from classes.globals import Globals
from classes.keybinds import Keybinds

from scenes.scene_base import SceneBase
from scripts.tilemap import TileMap

from utils.animation import *

class Editor(SceneBase):
    def __init__(self):
        super().__init__(2)

        self.index = 0
        self.variant = 0
        self.max_levels = 2
        self.max_worlds = 1
        self.current_level = 0
        self.current_world = 0

        self.modifiers = {
            "click": False,
            "right_click": False,
            "shift": False,
            "ctrl": False,
        }

        self.tilemap = TileMap(self)
        self.objects = list(self.tilemap.assets.keys())
        self.tilemap.load("./data/world0/levels/0.json")


    def render(self):
        """Renders the level that is currently being edited"""
        self._display.fill(Colors.black)
        self.tilemap.render()

        # Get the currently selected object
        asset = self.objects[self.index]
        preview_image = self.tilemap.assets[asset][self.variant].copy()
        preview_image.set_alpha(128)

        # Calculate the position of the object
        tile_x = int(Globals.mouse_position[0] / 2 // self.tilemap.tile_size)
        tile_y = int(Globals.mouse_position[1] / 2 // self.tilemap.tile_size)
        tile_location = str(tile_x) + ";" + str(tile_y)
        image_offset = (0, 0)
        if asset == "flag":
            image_offset = (0, 10)
        
        self._display.blit(preview_image, (tile_x * self.tilemap.tile_size - image_offset[0], 
                                           tile_y * self.tilemap.tile_size - image_offset[1]))

        # Place/delete objects
        if self.modifiers["click"]:
            # Only allow placing one flag of each type
            if asset == "flag":
                for tile_l in self.tilemap.tilemap:
                    tile = self.tilemap.tilemap[tile_l]
                    if tile["type"] == asset and tile["variant"] == self.variant:
                        del self.tilemap.tilemap[tile_l]
                        break

            self.tilemap.tilemap[tile_location] = {
                "type": asset, "variant": self.variant, 
                "position": [tile_x - image_offset[0] / self.tilemap.tile_size, tile_y - image_offset[1] / self.tilemap.tile_size]}


        if self.modifiers["right_click"] and tile_location in self.tilemap.tilemap:
            del self.tilemap.tilemap[tile_location]

    def keydown_event(self, key):
        """Runs whenever a keyboard button is pressed"""
        if key == pyg.K_F1:
            self.finished = True
            return
        elif key in Keybinds.binds["save"]:
            self.tilemap.save(f"./data/world{self.current_world}/levels/{self.current_level}.json")
            return
        elif key == pyg.K_F3:
            self.tilemap.save(f"./data/world{self.current_world}/levels/{self.current_level}.json")
            return self.current_level

        elif key == pyg.K_LSHIFT:
            self.modifiers["shift"] = True
            return
        elif key == pyg.K_LCTRL:
            self.modifiers["ctrl"] = True

        elif key == pyg.K_RIGHT:
            self.current_level += 1
        elif key == pyg.K_LEFT:
            self.current_level -= 1

        elif key == pyg.K_RETURN:
            if self.modifiers["ctrl"]:
                self.current_world = self.max_worlds
                self.max_worlds += 1
                self.current_level = 0
            else:
                self.current_level = self.max_levels
                self.max_levels += 1

        self.current_level %= self.max_levels
        try:
            self.tilemap.load(f"./data/world{self.current_world}/levels/{self.current_level}.json")
        except FileNotFoundError:
            self.tilemap.tilemap = {}
        
        # Clear level
        if key == pyg.K_F4:
            self.tilemap.tilemap = {}

    def keyup_event(self, key):
        """Runs whenever a keyboard button is released"""
        if key == pyg.K_LSHIFT:
            self.modifiers["shift"] = False
        elif key == pyg.K_LCTRL:
            self.modifiers["ctrl"] = False
        
    def mousedown_event(self, button, ):
        """Runs whenever a mouse button is pressed"""
        if button == 1:
            self.modifiers["click"] = True
        elif button == 3:
            self.modifiers["right_click"] = True

        elif button == 4:
            if self.modifiers["ctrl"]:
                self.current_level -= 1
                self.current_level %= self.max_levels
                self.tilemap.load(f"./data/world0/levels/{self.current_level}.json")
                return

            if self.modifiers["shift"]:
                self.variant += 1
            else:
                self.index += 1
                self.variant = 0

        elif button == 5:
            if self.modifiers["ctrl"]:
                self.current_level += 1
                self.current_level %= self.max_levels
                self.tilemap.load(f"./data/world0/levels/{self.current_level}.json")
                return
            if self.modifiers["shift"]:
                self.variant -= 1
            else:
                self.index -= 1
                self.variant = 0

        self.index %= len(self.objects)
        self.variant %= len(self.tilemap.assets[self.objects[self.index]])

    def mouseup_event(self, button):
        """Runs whenever a mouse button is released"""
        if button == 1:
            self.modifiers["click"] = False
        elif button == 3:
            self.modifiers["right_click"] = False