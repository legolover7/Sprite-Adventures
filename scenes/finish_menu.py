# Import statements
import pygame as pyg

# Classes
from classes.buttons import MenuButton
from classes.display import Colors, Fonts
from classes.globals import Globals

from scenes.scene_base import SceneBase

class FinishMenu(SceneBase):
    def __init__(self, settings_menu):
        super().__init__()
        self.settings_menu = settings_menu

    def render(self):
        self._display.fill(Colors.charcoal)

        text_width, text_height = Fonts.font_50.size("You Win!")
        self._display.blit(Fonts.font_50.render("You Win!", True, Colors.white), ((self._display.get_width() - text_width) / 2, (self._display.get_height() - text_height) / 2 - 200))

        text_width, text_height = Fonts.font_40.size("Deaths: " + str(Globals.player_data["deaths"]))
        self._display.blit(Fonts.font_40.render("Deaths: " + str(Globals.player_data["deaths"]), True, Colors.white), ((self._display.get_width() - text_width) / 2, (self._display.get_height() - text_height) / 2 - 100))

        text_width, text_height = Fonts.font_40.size("Coins collected: " + str(Globals.coins_collected))
        self._display.blit(Fonts.font_40.render("Coins collected: " + str(Globals.coins_collected), True, Colors.white), ((self._display.get_width() - text_width) / 2, (self._display.get_height() - text_height) / 2 - 60))

        text_width, text_height = Fonts.font_30.size("Press the enter key to continue")
        self._display.blit(Fonts.font_30.render("Press the enter key to continue", True, Colors.white), ((self._display.get_width() - text_width) / 2, (self._display.get_height() - text_height) / 2 + 100))

        if not self.settings_menu.data["show_timer"]:
            return

        # Show times
        seconds = Globals.player_data["playticks"] / 60
        minutes = seconds // 60
        hours = minutes // 60
        playtime = ""

        # Format string
        playtime += (str(int(hours)) + ":") if hours > 0 else ""
        playtime += ("0" if minutes % 60 < 10 else "") + str(int(minutes) % 60) + ":"
        playtime += ("0" if seconds % 60 < 10 else "") + str(round(seconds % 60, 2))
                
        text_width, text_height = Fonts.font_40.size("Time played: " + playtime)
        self._display.blit(Fonts.font_40.render("Time played: " + playtime, True, Colors.white), ((self._display.get_width() - text_width) / 2, (self._display.get_height() - text_height) / 2 - 20))

        offset = self._display.get_height()/2 + 150
        for t in range(5):
            seconds = Globals.player_data["times"][t] / 60
            minutes = seconds // 60
            playtime = ""

            # Format string
            playtime += ("0" if minutes % 60 < 10 else "") + str(int(minutes) % 60) + ":"
            playtime += ("0" if seconds % 60 < 10 else "") + str(round(seconds % 60, 2))
                
            text_width, text_height = Fonts.font_24.size("Level 1-" + str(t + 1) + ": " + playtime)
            self._display.blit(Fonts.font_24.render("Level 1-" + str(t + 1) + ": " + playtime, True, Colors.white), ((self._display.get_width() - text_width) / 2, offset))
            offset += text_height + 4

    def keydown_event(self, key):
        """Runs whenever a keyboard button is pressed"""
        if key == pyg.K_RETURN:
            return "Main Menu"