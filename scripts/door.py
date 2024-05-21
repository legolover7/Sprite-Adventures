import pygame as pyg

class Door:
    def __init__(self, world, position):
        self.x, self.y = position
        self.width, self.height = 20, 40
        self.world = world
        
        self.opened = False
        self.open_offset = 0
        self.display = pyg.Surface((self.width, self.height))
        self.display.set_colorkey((1, 1, 1))
        
        # Create door tiles in tilemap (for collision)
        self.tile1pos = str(int(self.x // self.world.tilemap.tile_size)) + ";" + str(int(self.y // self.world.tilemap.tile_size))
        self.tile2pos = str(int(self.x // self.world.tilemap.tile_size)) + ";" + str(int(self.y // self.world.tilemap.tile_size + 1))
        self.doorx = self.x // self.world.tilemap.tile_size
        self.doory = self.y // self.world.tilemap.tile_size
        
        self.world.tilemap.tilemap[self.tile1pos] = {"type": "door", "variant": 0, "position": [self.doorx, self.doory]}
        self.world.tilemap.tilemap[self.tile2pos] = {"type": "door", "variant": 0, "position": [self.doorx, self.doory + 1]}

    def rect(self):
        return pyg.Rect(self.x, self.y, self.width, self.height)
    
    def openclose(self):
        self.opened = not self.opened

    def render(self, surface: pyg.Surface):
        self.display.fill((1, 1, 1))
        self.display.blit(self.world.assets["door"], (0, 0 - self.open_offset))
        surface.blit(self.display, (self.x, self.y))

        if self.opened and self.open_offset < 38:
            self.open_offset += 1

            if self.tile1pos in self.world.tilemap.tilemap:
                del self.world.tilemap.tilemap[self.tile1pos]
                del self.world.tilemap.tilemap[self.tile2pos]
                
        elif not self.opened and self.open_offset > 0:
            self.open_offset -= 1

            self.world.tilemap.tilemap[self.tile1pos] = {"type": "door", "variant": 0, "position": [self.doorx, self.doory]}
            self.world.tilemap.tilemap[self.tile2pos] = {"type": "door", "variant": 0, "position": [self.doorx, self.doory + 1]}