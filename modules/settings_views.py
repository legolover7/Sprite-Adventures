import pygame as pyg

from classes.buttons import Checkbox, Dropdown
from classes.display import Colors, Fonts
from classes.globals import Globals

class View:
    def __init__(self):
        self.x, self.y = 200, 0
        self.width, self.height = Globals.WIDTH - 200, Globals.HEIGHT

        self._display = pyg.Surface((self.width, self.height))
        self.checkboxes = {}


    def draw_background(self):
        pyg.draw.rect(self._display, Colors.gray, (0, 0, self.width, self.height), border_radius=8)
        pyg.draw.rect(self._display, Colors.charcoal, (2, 2, self.width - 4, self.height - 4), border_radius=8)

    def render(self, window: pyg.Surface):
        self.draw_background()
        window.blit(self._display, (self.x, self.y))

    def click(self, mouse_position: list):
        pass

class GeneralV(View):
    def __init__(self):
        super().__init__()

        self.checkboxes = {
            "show_fps": Checkbox((70, 100, 20, 20), "Show FPS", Fonts.font_24, left_align=True),
            "show_timer": Checkbox((70, 130, 20, 20), "Show Timer", Fonts.font_24, left_align=True),
            "show_deaths": Checkbox((70, 160, 20, 20), "Show Deaths", Fonts.font_24, left_align=True),
        }

    def render(self, window: pyg.Surface):
        self.draw_background()

        for box in self.checkboxes:
            self.checkboxes[box].draw(self._display)

        window.blit(self._display, (self.x, self.y))

    def click(self, mouse_position: list):
        for box in self.checkboxes:
            if self.checkboxes[box].check_mcollision(mouse_position):
                self.checkboxes[box].active = not self.checkboxes[box].active
                return True
            
class DisplayV(View):
    def __init__(self):
        super().__init__()

        # self.dropdowns = {
        #     "resolution": Dropdown((70, 100, 200, 30), Fonts.font_20, ["1920x1080", "1065x600"])
        # }

    def render(self, window: pyg.Surface):
        self.draw_background()

        # for dd in self.dropdowns:
        #     self.dropdowns[dd].draw(self._display, Globals.mouse_position)

        window.blit(self._display, (self.x, self.y))
        
    # def click(self, mouse_position: list):
    #     previous_resolution = self.dropdowns["resolution"].selected_option
    #     self.dropdowns["resolution"].click(mouse_position)
    #     if self.dropdowns["resolution"].selected_option != previous_resolution:
    #         return self.dropdowns["resolution"].selected_option