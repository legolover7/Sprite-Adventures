# Import statements
import pygame as pyg

# Classes
from classes.buttons import MenuButton
from classes.display import Colors, Fonts
from classes.globals import Globals
from classes.keybinds import Keybinds

from scenes.scene_base import SceneBase
from scripts.tilemap import TileMap

import modules.collider as collider
import utils.utils as utils
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
        self.nodes = {}

        self.current_link = []

        self.name = "editor"
        self.modifiers = {
            "click": False,
            "right_click": False,
            "shift": False,
            "ctrl": False,
        }

        self.ui_display = pyg.Surface((200, Globals.WIDTH))
        self.ui_display.set_alpha(200)
        self.show_ui = True
        self.mode = "Place"

        self.tilemap = TileMap(self)
        self.objects = list(self.tilemap.assets.keys())
        self.tilemap.load("./data/world0/levels/0.json")

    def draw_ui(self):
        self.ui_display.fill(Colors.charcoal)
        
        # Draw modes
        text_width, text_height = Fonts.font_20.size("Placement mode")
        self.ui_display.blit(Fonts.font_20.render("Placement mode", True, Colors.white), (2, 40))
        if self.mode == "Place" or collider.collides_point(Globals.mouse_position, (0, 38, text_width + 4, text_height + 4)):
            pyg.draw.line(self.ui_display, Colors.white, (2, 60), (text_width, 60))


        text_width, text_height = Fonts.font_20.size("Linking mode")
        self.ui_display.blit(Fonts.font_20.render("Linking mode", True, Colors.white), (2, 70))
        if self.mode == "Link" or collider.collides_point(Globals.mouse_position, (0, 68, text_width + 4, text_height + 4)):
            pyg.draw.line(self.ui_display, Colors.white, (2, 90), (text_width, 90))
        
        
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
        
        if self.mode == "Place":
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
                tile = self.tilemap.tilemap[tile_location]
                # Remove doors from any linkages
                if tile["type"] == "door":
                    for link in self.tilemap.links:
                        if tile_location in self.tilemap.links[link]:
                            self.tilemap.links[link].remove(tile_location)

                elif tile["type"] == "button" and tile_location in self.tilemap.links:
                    del self.tilemap.links[tile_location]
                
                del self.tilemap.tilemap[tile_location]

        elif self.mode == "Link":
            if self.nodes == {}:
                for object in self.tilemap.extract([("button", 0), ("door", 0)], keep=True):
                    x, y = object["position"][0] + 10, object["position"][1] + 10
                    self.nodes[(x, y)] = object["type"]
                
            # Drag connections from node
            if self.modifiers["click"] and self.current_link == []:
                for node in self.nodes:
                    if collider.collides_point_circle((Globals.mouse_position[0] / 2, Globals.mouse_position[1] / 2), node, 3) and self.nodes[node] != "door":
                       self.current_link = node

            # Draw connection nodes
            for node in self.nodes:
                if self.nodes[node] == "button":
                    color = Colors.dark_green if collider.collides_point_circle((Globals.mouse_position[0] / 2, Globals.mouse_position[1] / 2), node, 3) else Colors.green
                elif self.nodes[node] == "door":
                    color = Colors.dark_yellow if collider.collides_point_circle((Globals.mouse_position[0] / 2, Globals.mouse_position[1] / 2), node, 3) else Colors.yellow
                pyg.draw.circle(self._display, color, node, 3)

            # Draw connection between current noded and mouse cursor
            if self.current_link != []:
                pyg.draw.line(self._display, Colors.aqua, self.current_link, (Globals.mouse_position[0] / 2, Globals.mouse_position[1] / 2))
            
            # Draw connections between objects
            for start_node in self.tilemap.links:
                sx, sy = utils.cvt_str_to_tile(start_node)
                for end_node in self.tilemap.links[start_node]:
                    fx, fy = utils.cvt_str_to_tile(end_node)
                    pyg.draw.line(self._display, Colors.aqua, (sx + 10, sy + 10), (fx + 10, fy + 10))

        self.draw_ui()

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

        elif key == pyg.K_LEFTBRACKET:
            self.show_ui = not self.show_ui

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
            # Check for if a different mode was pressed
            text_width, text_height = Fonts.font_20.size("Placement mode")
            if collider.collides_point(Globals.mouse_position, (0, 38, text_width + 4, text_height + 4)):
                self.mode = "Place"
                self.nodes = {}
                return

            text_width, text_height = Fonts.font_20.size("Linking mode")
            if collider.collides_point(Globals.mouse_position, (0, 68, text_width + 4, text_height + 4)):
                self.mode = "Link"
                return
            
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

            if self.mode == "Link":
                # Connect nodes
                if self.current_link != []:
                    for node in self.nodes:
                        if node == self.current_link: continue
                        
                        if collider.collides_point_circle((Globals.mouse_position[0] / 2, Globals.mouse_position[1] / 2), node, 3):
                            start = utils.cvt_tile_to_str(self.current_link)
                            end = utils.cvt_tile_to_str(node)
                            
                            # Add/remove/append node
                            if start in self.tilemap.links:
                                if end in self.tilemap.links[start]:
                                    self.tilemap.links[start].remove(end)
                                else:
                                    self.tilemap.links[start].append(end) 
                            else:
                                self.tilemap.links[start] = [end]

                    self.current_link = []

        elif button == 3:
            self.modifiers["right_click"] = False

            if self.mode == "Link":
                for node in self.tilemap.links.copy():
                    x, y = utils.cvt_str_to_tile(node)

                    if collider.collides_point_circle((Globals.mouse_position[0] / 2, Globals.mouse_position[1] / 2), (x + 10, y + 10), 3):
                        del self.tilemap.links[node]