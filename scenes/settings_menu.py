# Import statements
import pygame as pyg
import json
import os

# Classes
from classes.buttons import Button, Checkbox
from classes.display import Colors, Fonts
from classes.globals import FilePaths

from modules.settings_views import *
from scenes.scene_base import SceneBase

class SettingsMenu(SceneBase):
    def __init__(self):
        self.render_scale = 1
        super().__init__()

        self.back_button = Button((50, 30), (100, 30), Colors.gray, "Back")

        self.active = False
        self.transition = 0

        self.active_view = "general"
        self.views = {
            "general": GeneralV(),
            "display": DisplayV(),
            "keybinds": View(),
        }

        self.load()

    def load(self):
        """Loads the data from the settings file, if it exists, otherwise sets data to defaults"""
        self.data = {
            "views": [
                "General",
                "Display",
                "Keybinds",
            ],
            "show_fps": False,
            "show_timer": True,
            "show_deaths": False
        }
        
        if os.path.isfile(FilePaths.settings):
            with open(FilePaths.settings, "r") as file:
                try:
                    self.data = json.load(file)
                except json.decoder.JSONDecodeError:
                    pass

        for v in self.data["views"]:
            view = self.views[v.lower()]
            for b in view.checkboxes:
                box = view.checkboxes[b]
                box.active = self.data[b]

    def save(self):
        """Saves the data to the settings file"""
        with open(FilePaths.settings, "w") as file:
            file.write(json.dumps(self.data, indent=4))

    def render(self):
        """Draws this scene component"""
        # Draw background
        if self.active:
            self._display.fill(Colors.black)
        else:
            self._display.fill(Colors.charcoal)
        
        pyg.draw.rect(self._display, Colors.gray, (0, 0, 200, Globals.HEIGHT), border_radius=8)
        pyg.draw.rect(self._display, Colors.charcoal, (2, 2, 196, Globals.HEIGHT - 4), border_radius=8)

        # Draw sidebar
        self.back_button.draw(self._display)
        vertical_offset = 100
        for title in self.data["views"]:
            text_width = Fonts.font_24.size(title)[0]
            self._display.blit(Fonts.font_24.render(title, True, Colors.white), (100 - text_width/2, vertical_offset))

            # Underline if mouse is hovering
            rect = pyg.Rect(100 - text_width/2, vertical_offset - 2, text_width, 28)
            if rect.collidepoint(Globals.mouse_position[0], Globals.mouse_position[1]):
                pyg.draw.line(self._display, Colors.white, (100 - text_width/2, vertical_offset + 26),
                                                           (100 + text_width/2, vertical_offset + 26))
                
            vertical_offset += 35

        # Render currently active view
        self.views[self.active_view].render(self._display)
        title = self.active_view[0].capitalize() + self.active_view[1:]
        self._display.blit(Fonts.font_30.render(title, True, Colors.white), (230, 20))

    def keydown_event(self, key):
        """Runs whenever a keyboard button is pressed"""
        if key == pyg.K_F1:
            self.finished = True

    def mousedown_event(self, button):
        """Runs whenever a mouse button is pressed"""
        if button == 1:
            if self.back_button.check_mcollision():
                return "Main Menu"

        # Check sidebar text clicked
        vertical_offset = 100
        for title in self.data["views"]:
            text_width = Fonts.font_24.size(title)[0]

            rect = pyg.Rect(100 - text_width/2, vertical_offset - 2, text_width, 28)
            if rect.collidepoint(Globals.mouse_position[0], Globals.mouse_position[1]):
                self.active_view = title.lower()
                return
                
            vertical_offset += 35
            
        mouse_position = Globals.mouse_position.copy()
        mouse_position[0] -= 200
        if self.views[self.active_view].click(mouse_position):
            for v in self.data["views"]:
                view = self.views[v.lower()]
                for b in view.checkboxes:
                    box = view.checkboxes[b]
                    self.data[b] = box.active