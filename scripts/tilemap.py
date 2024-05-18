# Import statements
import pygame as pyg
import json

# Classes
from classes.display import Colors, Fonts
from classes.globals import Globals
from utils.animation import load_images

NEIGHBOR_OFFSETS = []

for x in range(-2, 3):
    for y in range(-2, 3):
        NEIGHBOR_OFFSETS.append((x, y))

PHYSICS_TILES = {"steel"}

class TileMap:
    def __init__(self, world):
        self.world = world

        self.tilemap = {}
        self.tile_size = 20
        self.offgrid_tiles = []

        self.assets = {
            "steel": load_images("tiles/steel"),
            "flag": load_images("tiles/flag"),
            "lava": load_images("tiles/lava"),
            "coin": load_images("objects/coin")
        }

    def extract(self, id_pairs, keep=False):
        matches = []
        for tile in self.offgrid_tiles.copy():
            if (tile["type"], tile["variant"]) in id_pairs:
                matches.append(tile.copy())
                if not keep:
                    self.offgrid_tiles.remove(tile)
                    
        for loc in self.tilemap.copy():
            tile = self.tilemap[loc]
            if (tile["type"], tile["variant"]) in id_pairs:
                matches.append(tile.copy())
                matches[-1]["position"] = matches[-1]["position"].copy()
                matches[-1]["position"][0] *= self.tile_size
                matches[-1]["position"][1] *= self.tile_size
                if not keep:
                    del self.tilemap[loc]
        
        return matches

    def tiles_around(self, position):
        """Gets the tiles in a 1x1 square radius"""
        tiles = []
        tile_loc = (int(position[0] // self.tile_size), int(position[1] // self.tile_size))
        for offset in NEIGHBOR_OFFSETS:
            check_loc = str(tile_loc[0] + offset[0]) + ';' + str(tile_loc[1] + offset[1])
            if check_loc in self.tilemap:
                tiles.append(self.tilemap[check_loc])
        return tiles
    
    def save(self, path):
        """Saves the current tilemap to the desired path"""
        with open(path, "w") as file:
            json.dump({'tilemap': self.tilemap, 'tile_size': self.tile_size, 
                       'offgrid': self.offgrid_tiles}, file)
        
    def load(self, path):
        """Loads the current tilemap from the desired path"""
        with open(path, "r") as file:
            map_data = json.load(file)
        
        self.tilemap = map_data['tilemap']
        self.tile_size = map_data['tile_size']
        self.offgrid_tiles = map_data['offgrid']
        
    def solid_check(self, position):
        """Checks if the provided position has a tile placed there"""
        tile_location = str(int(position[0] // self.tile_size)) + ';' 
        tile_location += str(int(position[1] // self.tile_size))
        
        if tile_location in self.tilemap:
            if self.tilemap[tile_location]["type"] in PHYSICS_TILES:
                return self.tilemap[tile_location]
    
    def physics_rects_around(self, position):
        """Returns the tiles that have collision properties in a 1x1 square radius"""
        rects = []
        for tile in self.tiles_around(position):
            if tile["type"] in PHYSICS_TILES:
                rects.append(pyg.Rect(tile['position'][0] * self.tile_size, 
                                      tile['position'][1] * self.tile_size, 
                                      self.tile_size, self.tile_size))
        return rects

    def render(self):
        """Renders the tiles to the screen"""
        for tile_location in self.tilemap:
            tile = self.tilemap[tile_location]
            self.world._display.blit(self.assets[tile["type"]][tile["variant"]], 
                                     (tile["position"][0] * self.tile_size, 
                                      tile["position"][1] * self.tile_size))