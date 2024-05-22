from scripts.tilemap import TileMap

class UndoRedo:
    def __init__(self, tilemap: TileMap):
        self.tiles = {}
        self.action = "replace"
        self.tilemap = tilemap

    def activate(self):
        if self.action == "replace":
            for tile in self.tiles:
                self.tilemap.tilemap[tile] = self.tiles[tile]

        elif self.action == "remove":
            for tile in self.tiles:
                if tile in self.tilemap.tilemap.copy():
                    del self.tilemap.tilemap[tile]