
from scripts.button import Button
from scripts.door import Door

class Connection:
    def __init__(self):
        self.buttons = []
        # OR means any button activates object, AND means all buttons must be activated
        self.mode = "OR"

    def connect(self, buttons: list[Button], objects: list[Door]):
        self.buttons = buttons
        self.objects = objects

    def press(self, button: Button):
        """Activates all of the objects connected to a given button"""
        
        if self.mode == "OR":
            if button in self.buttons:
                for object in self.objects:
                    object.opened = True

    def unpress(self, fast=False):
        for button in self.buttons:
            button.pressed = False
        for object in self.objects:
            object.opened = False
            if fast:
                object.open_offset = 0