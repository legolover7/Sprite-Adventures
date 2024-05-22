import pygame as pyg
import os

BASE_IMG_PATH = 'assets/'

def load_image(path):
    img = pyg.image.load(BASE_IMG_PATH + path).convert()
    img.set_colorkey((1, 1, 1))
    return img

def load_images(path):
    images = []
    for img_name in sorted(os.listdir(BASE_IMG_PATH + path)):
        images.append(load_image(path + '/' + img_name))
    return images

def load_sound(path):
    return pyg.mixer.Sound(BASE_IMG_PATH + path)

def play_sound(sound):
    pyg.mixer.Sound.play(sound)

class Animation:
    def __init__(self, images, img_dur=5, loop=True):
        self.images = images
        self.loop = loop
        self.imgage_duration = img_dur
        self.done = False
        self.frame = 0
    
    def copy(self):
        return Animation(self.images, self.imgage_duration, self.loop)
    
    def update(self):
        if self.loop:
            self.frame = (self.frame + 1) % (self.imgage_duration * len(self.images))
        else:
            self.frame = min(self.frame + 1, self.imgage_duration * len(self.images) - 1)
            if self.frame >= self.imgage_duration * len(self.images) - 1:
                self.done = True
    
    def image(self):
        return self.images[int(self.frame / self.imgage_duration)]