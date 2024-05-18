import pygame as pyg

from classes.globals import Globals
from scripts.tilemap import TileMap

from utils.animation import Animation

class PhysicsEntity:
    def __init__(self, world, position, size, type):
        self.world = world
        self.x, self.y = position
        self.width, self.height = size
        self.type = type

        self.action = ''
        self.animation_offset = (0, 0)
        self.flip = False
        self.died = False
        self.respawn = 0
        self.walking = False
        self.set_action("idle")
        
        self.velocity = [0, 0]
        self.last_movement = [0, 0]

    def rect(self):
        return pyg.Rect(self.x, self.y, self.width, self.height)

    def update(self, tilemap: TileMap, movement):
        self.collisions = {"up": False, "down": False, "right": False, "left": False}
        
        if self.walking:
            movement[0] *= 0.5
            
        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])

        # Kill entity if it's too low
        if self.y > Globals.HEIGHT / 2 + 50 and not self.died:
            if self.type == "player":
                self.respawn = 60
                Globals.player_data["deaths"] += 1

        # Compute x collisions
        self.x += frame_movement[0]
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around((self.x, self.y)):
            if entity_rect.colliderect(rect):
                if frame_movement[0] > 0:
                    entity_rect.right = rect.left
                    self.collisions['right'] = True
                if frame_movement[0] < 0:
                    entity_rect.left = rect.right
                    self.collisions['left'] = True
                self.x = entity_rect.x
        
        # Compute y collisions
        self.y += frame_movement[1]
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around((self.x, self.y)):
            if entity_rect.colliderect(rect):
                if frame_movement[1] > 0:
                    entity_rect.bottom = rect.top
                    self.collisions['down'] = True
                if frame_movement[1] < 0:
                    entity_rect.top = rect.bottom
                    self.collisions['up'] = True
                self.y = entity_rect.y

        # Set direction
        if movement[0] > 0:
            self.flip = False
        if movement[0] < 0:
            self.flip = True

        self.last_movement = movement

        self.velocity[1] = min(6, self.velocity[1] + 0.11)

        if self.collisions["down"] or self.collisions["up"]:
            self.velocity[1] = 0

        self.animation.update()

    def set_action(self, action):
        """Changes the current animation of the entity"""
        if action != self.action:
            self.action = action
            self.animation = self.world.assets[self.type + '/' + self.action].copy()

    def render(self, surface: pyg.Surface, offset=(0, 0)):
        surface.blit(pyg.transform.flip(self.animation.image(), self.flip, False), 
                     (self.x - offset[0] + self.animation_offset[0], 
                      self.y - offset[1] + self.animation_offset[1]))

class Player(PhysicsEntity):
    def __init__(self, world, position, size):
        super().__init__(world, position, size, "player")
        
        self.jumps = 1
        self.air_time = 0
        self.wall_slide = False
        self.walljump = 0
        self.num_coins = 0

    def update(self, tilemap, movement=(0, 0)):
        """Does physics updates on the player"""
        super().update(tilemap, movement=movement)
        
        self.air_time += 1

        if self.collisions['down']:
            self.air_time = 0
            self.jumps = 1

        self.wall_slide = False
        if (self.collisions["right"] or self.collisions["left"]) and self.air_time > 4:
            self.wall_slide = True
            self.velocity[1] = min(self.velocity[1], 0.5)
            if self.collisions["right"]:
                self.flip = False
            else:
                self.flip = True
            self.set_action('wall_slide')
        
        if not self.wall_slide:
            if self.air_time > 4:
                self.set_action("fall")
            elif movement[0] != 0 and not self.walking:
                self.set_action("run")
            elif movement[0] != 0:
                self.set_action("walk")
            else:
                self.set_action("idle")

        if self.velocity[0] > 0:
            self.velocity[0] = max(self.velocity[0] - 0.1, 0)
        else:
            self.velocity[0] = min(self.velocity[0] + 0.1, 0)
    
    def jump(self):
        """Causes the player to jump by giving it upwards force"""
        jump_force = -3.6
        kickback_force = 2.5

        if self.wall_slide:
            if self.flip and self.last_movement[0] < 0:
                self.velocity[0] = kickback_force
                self.velocity[1] = jump_force * 0.8
                self.air_time = 5
                self.jumps = max(0, self.jumps - 1)
                self.walljump = 20
                return True
            
            elif not self.flip and self.last_movement[0] > 0:
                self.velocity[0] = -kickback_force
                self.velocity[1] = jump_force * 0.8
                self.air_time = 5
                self.jumps = max(0, self.jumps - 1)
                self.walljump = 20
                return True

        elif self.jumps and self.air_time < 8:
            self.jumps -= 1
            self.velocity[1] = jump_force
            self.air_time = 5
            return True