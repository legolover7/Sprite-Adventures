# Import statements
import pygame as pyg

# Classes
from classes.buttons import MenuButton
from classes.display import Colors, Fonts
from classes.globals import Globals

from scenes.scene_base import SceneBase

class MainMenu(SceneBase):
    """The main menu page that the user opens on startup"""

    def __init__(self):
        """Initializes the main menu components"""
        self.render_scale = 1
        super().__init__()

        self.centerx = Globals.WIDTH / 2 / self.render_scale
        self.centery = Globals.HEIGHT / 2 / self.render_scale

        self.buttons = {}

        spacing = 0
        if Globals.player_data["playticks"] != 0:
            spacing = 50

        self.buttons["new_game"] = MenuButton((self.centerx - 300, self.centery - 150 - spacing), (600, 70), "New Game")
        self.buttons["editor"]   = MenuButton((self.centerx - 300, self.centery - 50 + spacing),  (600, 70), "Editor")
        self.buttons["settings"] = MenuButton((self.centerx - 300, self.centery + 50 + spacing),  (600, 70), "Settings")
        self.buttons["quit"]     = MenuButton((self.centerx - 300, self.centery + 150 + spacing), (600, 70), "Quit")

        if Globals.player_data["playticks"] != 0:
            self.buttons["continue_game"] = MenuButton((self.centerx - 300, self.centery - 100), (600, 70), "Continue Game")

    def render(self):
        """Draws this scene component"""
        self._display.fill(Colors.charcoal)

        text_width = Fonts.font_50.size("Sprite Adventures")[0]
        self._display.blit(Fonts.font_50.render("Sprite Adventures", True, Colors.white), (Globals.WIDTH/2 - text_width/2, 50))

        for button in self.buttons:
            self.buttons[button].draw(self._display)

    def keydown_event(self, key):
        """Runs whenever a keyboard button is pressed"""
        if key == pyg.K_RETURN:
            return "New Game"

    def mousedown_event(self, button):
        """Runs whenever a mouse button is pressed"""
        if button == 1:
            # Check for button collisions
            for button in self.buttons:
                if self.buttons[button].check_mcollision():
                    if self.buttons[button].text == "Quit":
                        self.finished = True
                    return self.buttons[button].text