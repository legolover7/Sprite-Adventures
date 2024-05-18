import pygame as pyg

class Keybinds:
    binds = {
        "move_left":    [pyg.K_a, pyg.K_LEFT],
        "move_right":   [pyg.K_d, pyg.K_RIGHT],
        "jump":         [pyg.K_SPACE, pyg.K_UP],
        "save":         [pyg.K_F2]
    }