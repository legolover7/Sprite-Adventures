import pygame as pyg

from classes.display import Colors, Fonts
from classes.globals import Globals
import modules.collider as collider
import modules.chunk_text as chunk_text

class Button:
    """A clickable and hoverable button
    
    Attributes:
        x, y: This object's x and y position.
        width, height: This object's size.        
        text: The text this button displays.
        font: The font that this object displays with (Defaults to font_20).
        text_color: The color of the text (Defaults to white).

    - For the draw and collision functions, passing in a "mouse_position" will
        override the usage of the global mouse position
    """
    def __init__(self, position: tuple, size: tuple, button_color: tuple, text: str):
        self.x, self.y = position
        self.width, self.height = size
        self.button_color = button_color
        self.text = text
        self.font = Fonts.font_20
        self.text_color = Colors.white

    def draw(self, window: pyg.Surface, mouse_position: list=[0, 0]):
        """Draws this button to the screen"""
        position = mouse_position if mouse_position != [0, 0] else Globals.mouse_position
        
        back_color = [self.button_color[i] * 0.8 for i in range(len(self.button_color))]
        
        # Draw body of button
        if not self.check_mcollision(position):
            pyg.draw.rect(window, back_color, (self.x+2, self.y+2, self.width, self.height), border_radius=5)
        color = back_color if self.check_mcollision(position) else self.button_color
        pyg.draw.rect(window, color, (self.x, self.y, self.width, self.height), border_radius=5)

        # Draw text of button
        text_width, text_height = self.font.size(self.text)
        window.blit(self.font.render(self.text, True, self.text_color), (self.x + (self.width - text_width)/2, self.y + (self.height - text_height)/2))

    def check_mcollision(self, mouse_position: list=[0, 0]):
        """Returns true if the mouse is hovering this button"""
        m = mouse_position if mouse_position != [0, 0] else Globals.mouse_position
        return collider.collides_point(m, (self.x, self.y, self.width, self.height))
    
class MenuButton(Button):
    """A specific implementation of a button"""
    def __init__(self, position, size, text):
        super().__init__(position, size, None, text)
        self.font = Fonts.font_30

    def draw(self, window: pyg.Surface):
        """Draws this button to the screen"""
        x, y = self.x, self.y
        width, height = self.width, self.height
        self.font = Fonts.font_30

        # Make button larger if hovered
        if self.check_mcollision():
            width *= 1.1
            height *= 1.1
            x -= (width - self.width) / 2
            y -= (height - self.height) / 2
            self.font = Fonts.font_32

        # Draw body
        pyg.draw.rect(window, Colors.light_gray, (x, y, width, height), border_radius=10)
        pyg.draw.rect(window, Colors.dark_gray, (x + 2, y + 2, width - 4, height - 4), border_radius=10)

        # Draw text
        text_width, text_height = self.font.size(self.text)
        window.blit(self.font.render(self.text, True, Colors.white), (self.x + (self.width - text_width) / 2, self.y + (self.height - text_height) / 2))

class ToolTip:
    def __init__(self, text: str, delay: int, max_width: int=0):
        self.text = text
        self.max_width = max_width
        if self.max_width == 0:
            self.max_width = Fonts.font_18.size(self.text)[0]

        self.max_width = min(self.max_width, Fonts.font_18.size(self.text)[0] + 10)

        self.displayed = False
        self.min_delay = delay
        self.current_delay = 0

    def draw(self, window: pyg.Surface, position: tuple):
        x, y = position

        text_lines = chunk_text.chunk(self.text, content_width=self.max_width, char_width=Fonts.font_18.size("A")[0])
        text_width, text_height = 0, Fonts.font_18.size("A")[1]
        for line in text_lines:
            line_width = Fonts.font_18.size(line)[0]
            if line_width > text_width:
                text_width = line_width
        
        pyg.draw.rect(window, Colors.dark_gray, (x, y, text_width + 6, (text_height + 2) * len(text_lines) + 4), border_radius=4)
        pyg.draw.rect(window, Colors.black, (x + 1, y + 1, text_width + 4, (text_height + 2) * len(text_lines) + 2), border_radius=4)

        for i in range(len(text_lines)):
            window.blit(Fonts.font_18.render(text_lines[i], True, Colors.white), (x + 3, y + 3 + (text_height + 2) * i))


class Checkbox:
    def __init__(self, rect, text, font , value="", default_active=False, left_align=False, tooltip: ToolTip=None):
        self.x, self.y, self.width, self.height = rect
        self.text = text
        self.font = font
        self.active = default_active
        self.left_align = left_align
        self.value = value
        self.tooltip = tooltip
    
    def draw(self, window: pyg.Surface):
        color = Colors.green if self.active else Colors.gray

        text_width = self.font.size(self.text)[0]
        content_width = text_width + self.width

        if self.left_align:
            window.blit(self.font.render(self.text, True, Colors.white), (self.x, self.y))

            pyg.draw.rect(window, Colors.gray, (self.x + text_width + 9, self.y - 1, self.width+2, self.height+2), border_radius=2)
            pyg.draw.rect(window, color, (self.x + text_width + 10, self.y, self.width, self.height), border_radius=2)
        else:
            pyg.draw.rect(window, Colors.gray, (self.x-1, self.y-1, self.width+2, self.height+2), border_radius=2)
            pyg.draw.rect(window, color, (self.x, self.y, self.width, self.height), border_radius=2)

            window.blit(self.font.render(self.text, True, Colors.white), (self.x - text_width -6, self.y))

        # Show tooltip on hover
        if self.tooltip != None:
            if not collider.collides_point(Globals.mouse_position, (self.x, self.y, content_width + 10, self.height)):
                self.tooltip.current_delay = 0
            else:
                self.tooltip.current_delay = min(self.tooltip.min_delay, self.tooltip.current_delay + 1)

    def check_mcollision(self, point: list=[0, 0]):
        m = point if point != [0, 0] else Globals.mouse_position
        if self.left_align:
            text_width = self.font.size(self.text)[0]
            return collider.collides_point(m, (self.x + text_width + 10, self.y, self.width, self.height))

        else:
            return collider.collides_point(m, (self.x, self.y, self.width, self.height))

class Dropdown:
    def __init__(self, rect: tuple, font: pyg.font.Font, options: list[str]):
        self.x, self.y, self.width, self.height = rect
        self.options = options
        self.font = font
        self.active = False
        self.selected_option = options[0]

    def draw(self, window: pyg.Surface, mouse_position: list):
        """Draws the dropdown based on whether it's active or not"""
        # Dropdown shown
        color = Colors.dark_gray
        if self.active:
            back_color = [color[i] * 0.8 for i in range(len(color))]
            highlight_color = [color[i] * 1.2 for i in range(len(color))]

            char_height = self.font.size("A")[1]
            # Draw background
            pyg.draw.rect(window, color, (self.x-2, self.y-2, self.width, self.height + (char_height + 2) * len(self.options) + 4), border_radius=5)
            
            # Draw currently selected option
            text_width, text_height = self.font.size(self.selected_option)
            vertical_offset = self.y + (self.height - text_height)/2
            window.blit(self.font.render(self.selected_option, True, Colors.white), (self.x + (self.width - text_width - 20)/2, vertical_offset))
            vertical_offset += text_height + 2
            pyg.draw.rect(window, back_color, (self.x, vertical_offset, self.width - 4, 2))
            vertical_offset += 4

            # Draw list of options
            for option in self.options: 
                text_width, text_height = self.font.size(option)
                # Highlight hovered option
                if collider.collides_point(mouse_position, (self.x, vertical_offset - 2, self.width - 8, text_height + 4)):
                    pyg.draw.rect(window, highlight_color, (self.x, vertical_offset - 2, self.width - 8, text_height + 4), border_radius=5)
                    
                window.blit(self.font.render(option, True, Colors.white), (self.x + (self.width - text_width - 20)/2, vertical_offset))
                vertical_offset += text_height + 2
        # Just the selected item
        else:
            if self.check_mcollision(mouse_position):
                color = [color[i] * 1.2 for i in range(len(color))]
            pyg.draw.rect(window, color, (self.x-2, self.y-2, self.width, self.height), border_radius=5)
            text_width, text_height = self.font.size(self.selected_option)
            window.blit(self.font.render(self.selected_option, True, Colors.white), (self.x + (self.width - text_width - 20)/2, self.y + (self.height - text_height)/2))

            # Draw down arrow
            pyg.draw.line(window, Colors.white, (self.x + self.width - 20, self.y + 8), (self.x + self.width - 15, self.y + self.height - 12), 1)
            pyg.draw.line(window, Colors.white, (self.x + self.width - 15, self.y + self.height - 12), (self.x + self.width - 10, self.y + 8), 1)

    
    def check_mcollision(self, point: list=[0, 0]):
        m = point if point != [0, 0] else Globals.mouse_position
        return collider.collides_point(m, (self.x, self.y, self.width, self.height))
    
    def click(self, point: list=[0, 0]):
        """Simulates a click and returns true if it was clicked, the option if it was active and an option was clicked, and None otherwise"""
        m = point if point != [0, 0] else Globals.mouse_position

        if self.check_mcollision(m):
            self.active = not self.active
            return True
        
        if not self.active: return
        
        # Calculate starting position
        text_height = self.font.size(self.selected_option)[1]
        vertical_offset = self.y + (self.height - text_height)/2 + text_height + 6
        # Check if a given option was selected
        for option in self.options:
            text_height = self.font.size(option)[1]
            # Highlight hovered option
            if collider.collides_point(m, (self.x, vertical_offset - 2, self.width - 8, text_height + 4)):
                self.selected_option = option
                self.active = False
                return option
            vertical_offset += text_height + 2