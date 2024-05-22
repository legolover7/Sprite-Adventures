import pygame as pyg
pyg.init()

from utils.animation import load_sound

class Globals:
    # Default size of the application
    WIDTH, HEIGHT = (1920, 1080)
    # User's monitor size
    WINDOW_WIDTH, WINDOW_HEIGHT = (0, 0)
    # Actual window object that gets displayed to the user
    WINDOW = pyg.Surface((0, 0))
    VID_BUFFER = pyg.Surface((WIDTH, HEIGHT))

    # Max FPS of application
    FPS = 60
    # Pygame clock object for controlling the framerate
    clock = pyg.time.Clock()

    # Current position of mouse cursor
    mouse_position = [0, 0]
    player_data = {}
    coins_collected = 0

    VERSION = "0.4.2"

class Sounds:
    sfx = {
        "coin_pickup": load_sound("sounds/pickupCoin.wav"),
        "player_jump": load_sound("sounds/jump.wav"),
        "button_press": load_sound("sounds/pressButton.wav"),
        "lava_death": load_sound("sounds/lavaDeath.wav"),
        "level_complete": load_sound("sounds/levelComplete.wav"),
    }

class FilePaths:
    settings = "./data/settings.json"
    player = "./data/player.json"