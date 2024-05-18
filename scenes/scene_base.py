import pygame as pyg

from classes.globals import Globals

class SceneBase:
    """
    
    Attributes:
        finished: When true, the application is done and we can quit
        settings_active: Whether or not the settings overlay is shown
    """
    def __init__(self, render_scale=1):
        self.finished = False
        self.overlay_active = False
        self.settings_active = False
        self._display = pyg.Surface((Globals.WIDTH // render_scale, Globals.HEIGHT // render_scale))
        
    def update(self):
        pass


    def keydown_event(self, key):
        """Runs whenever a keyboard button is pressed"""
        pass

    def keyup_event(self, key):
        """Runs whenever a keyboard button is released"""
        pass
        
    def mousedown_event(self, button):
        """Runs whenever a mouse button is pressed"""
        pass

    def mouseup_event(self, button):
        """Runs whenever a mouse button is released"""
        pass