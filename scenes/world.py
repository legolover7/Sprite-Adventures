# Import statements
import pygame as pyg

# Classes
from classes.display import Colors, Fonts
from classes.globals import Globals
from classes.keybinds import Keybinds

from scenes.scene_base import SceneBase
from scripts.coin import Coin
from scripts.entities import Player
from scripts.tilemap import TileMap
from scenes.settings_menu import SettingsMenu

# Modules
from utils.animation import *

class World(SceneBase):
    def __init__(self, settings_menu: SettingsMenu):
        super().__init__(2)

        self.assets = {
            "blank": load_image("blank.png"),
            "player/dead": Animation(load_images("player/dead")),
            "player/dissolve": Animation(load_images("player/dissolve"), loop=False),
            "player/duck": Animation(load_images("player/duck")),
            "player/fall": Animation(load_images("player/fall"), loop=False),
            "player/idle": Animation(load_images("player/idle"), img_dur=10),
            "player/walk": Animation(load_images("player/walk"), img_dur=10),
            "player/run": Animation(load_images("player/run"), img_dur=6),
            "player/slash": Animation(load_images("player/slash"), img_dur=6),
            "player/wall_slide": Animation(load_images("player/wall_slide"), loop=False),
            "coin": Animation(load_images("objects/coin"), img_dur=10)
        }

        self.reset()

        self.tilemap = TileMap(self)
        self.settings_menu = settings_menu

    def reset(self):
        self.movement = [False, False, False, False]
        self.player = Player(self, (50, 50), (16, 28))
        self.reset_position = [0, 0]
        self.current_world = 0
        self.current_level = 0
        self.transition = 0
        self.max_levels = 5
        self.next_level = False
        self.settings_active = False
        self.enter_time = 0
        self.overlay_active = False

    def load_level(self, world_id = 0, level_id: int = 0):
        """Loads a level based on the provided world and level ID"""
        try:
            self.coins = []
            self.coin_pickups = []
            self.tilemap.load(f"./data/world{world_id}/levels/{level_id}.json")
            pyg.display.set_caption(f"Sprite Adventure {world_id + 1}-{level_id + 1}")

            Globals.player_data["current_world"] = world_id
            Globals.player_data["current_level"] = level_id

            for flag in self.tilemap.extract([("flag", 0)]):
                self.player.x, self.player.y = flag["position"]
                self.reset_position = flag["position"]
                self.player.air_time = 0

            for coin in self.tilemap.extract([("coin", 0)]):
                self.coins.append(Coin(self, coin["position"]))
                self.coin_pickups.append(Coin(self, coin["position"]))
                
        except FileNotFoundError:
            pass

    def render(self):
        """Draws this scene component"""
        self._display.fill(Colors.charcoal)

        self.tilemap.render()

        self.player.render(self._display)

        for coin in self.coin_pickups:
            coin.render(self._display)

        # Transition for levels/player death
        if self.transition > 0 or self.player.respawn:
            transition_surf = pygame.Surface(self._display.get_size())
            pygame.draw.circle(transition_surf, (255, 255, 255), (self._display.get_width() // 2, self._display.get_height() // 2), (30 - abs(self.transition)) * 20)
            transition_surf.set_colorkey((255, 255, 255))
            self._display.blit(transition_surf, (0, 0))
            self.transition = max(0, self.transition - 1)

            if self.player.respawn > 30:
                self.transition += 2
            else:
                if self.next_level:
                    self.load_level(self.current_world, self.current_level)
                    self.next_level = False
                    Globals.player_data["times"][self.current_level - 1] = Globals.player_data["playticks"] - self.enter_time
                    
                self.player.x, self.player.y = self.reset_position
                self.player.velocity = [0, 0]
                Globals.coins_collected -= len(self.coins) - len(self.coin_pickups)
                self.coin_pickups = self.coins.copy()
                self.enter_time = Globals.player_data["playticks"]

    def update(self):
        if self.player.respawn < 30:
            self.player.died = False
        
        # Update coins
        for coin in self.coin_pickups:
            coin.animation.update()
            player_rect = self.player.rect()
            if player_rect.colliderect(coin.rect()):
                self.coin_pickups.remove(coin)
                Globals.coins_collected += 1

        # Update player
        if not self.transition:
            movement = [(self.movement[3] - self.movement[1]) * 2, self.movement[2] - self.movement[0]]
            self.player.update(self.tilemap, movement)
        else:
            self.player.animation.update()

        # Respawning the player
        if self.player.respawn and not self.player.died:
            self.player.air_time = 0
            self.player.set_action("idle")
            self.player.died = True
        self.player.respawn = max(0, self.player.respawn - 1)

        # Player reached the end
        for flag in self.tilemap.extract([("flag", 1)], keep=True):
            player_rect = self.player.rect()
            flag_rect = pyg.Rect(flag["position"][0], flag["position"][1], 20, 30)
            if player_rect.colliderect(flag_rect) and not self.next_level:
                self.current_level += 1
                self.current_level %= self.max_levels
                if self.current_level == 0:
                    Globals.player_data["times"][-1] = Globals.player_data["playticks"] - self.enter_time
                    return "Finish"
                self.player.respawn = 60
                self.next_level = True
                self.player.set_action("idle")

        # Player tile collisions
        for tile in self.tilemap.tiles_around((self.player.x, self.player.y)):
            player_rect = self.player.rect()
            tile_rect = pyg.Rect(tile["position"][0] * self.tilemap.tile_size, tile["position"][1] * self.tilemap.tile_size, 20, 20)
            if not player_rect.colliderect(tile_rect):
                continue
            
            # Hazards
            if tile["type"] == "lava" and not self.player.died:
                self.player.respawn = 60
                self.player.died = True
                Globals.player_data["deaths"] += 1
                self.player.set_action("dissolve")


    def keydown_event(self, key):
        """Runs whenever a keyboard button is pressed"""
        if key == pyg.K_F1:
            self.finished = True

        elif key == pyg.K_F3:
            return self.current_level

        # Movement keys
        if not self.overlay_active:
            if key in Keybinds.binds["move_left"]:
                self.movement[1] = True
            elif key in Keybinds.binds["move_right"]:
                self.movement[3] = True

            elif key in Keybinds.binds["jump"]:
                self.player.jump()

            elif key == pyg.K_LCTRL:
                self.player.walking = True

        if key == pyg.K_ESCAPE:
            self.settings_active = not self.settings_active

    def keyup_event(self, key):
        """Runs whenever a keyboard button is released"""
        
        # Movement keys
        if key in Keybinds.binds["move_left"]:
            self.movement[1] = False
        elif key in Keybinds.binds["move_right"]:
            self.movement[3] = False

        elif key == pyg.K_LCTRL:
            self.player.walking = False

    def mousedown_event(self, button):
        if self.settings_menu.active:
            return self.settings_menu.mousedown_event(button)