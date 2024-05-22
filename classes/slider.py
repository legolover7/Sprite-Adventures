import pygame as pyg

from classes.display import Colors, Fonts
import modules.collider as collider

class Slider:
    def __init__(self, position, size, text, progress=.5):
        self.x, self.y = position
        self.width, self.height = size
        self.text = text
        self.progress = progress
        self.clicked = False

    def render(self, window: pyg.Surface, mouse_position: list):
        # Calculate percentage
        if self.clicked:
            self.progress = (mouse_position[0] - self.x) / self.width
            
            self.progress = max(0, min(1, self.progress))

        # Progress bar
        pyg.draw.rect(window, Colors.light_gray, (self.x, self.y, self.width, self.height), border_radius=5)
        pyg.draw.rect(window, Colors.charcoal, (self.x + 2, self.y + 2, self.width - 4, self.height - 4), border_radius=5)
        pyg.draw.rect(window, Colors.dark_gray, (self.x + 2, self.y + 2, (self.width - 4) * self.progress, self.height - 4), border_radius=5)

        # Title and percentage
        text_width, text_height = Fonts.font_24.size(self.text)
        window.blit(Fonts.font_24.render(self.text, True, Colors.white), (self.x + (self.width - text_width) / 2, self.y - text_height))

        percentage = str(round(self.progress * 100, 2))
        text_width, text_height = Fonts.font_20.size(percentage + "%")
        window.blit(Fonts.font_20.render(percentage + "%", True, Colors.white), (self.x + (self.width - text_width) / 2, self.y + (self.height - text_height) / 2))

    def check_mdown(self, mouse_position: list):
        if collider.collides_point(mouse_position, (self.x, self.y, self.width, self.height)):
            self.clicked = True