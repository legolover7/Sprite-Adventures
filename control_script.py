# Import statements
import pygame as pyg
import json
import sys
import os

# Custom modules
from classes.display import Colors, Fonts
from classes.globals import Globals, FilePaths

from scenes.finish_menu import FinishMenu
from scenes.main_menu import MainMenu
from scenes.settings_menu import SettingsMenu
from scenes.editor import Editor
from scenes.world import World

from utils.profiler import Profiler

# Initialize window
pyg.init()
info_object = pyg.display.Info()
Globals.WIDTH, Globals.HEIGHT = (1920, 1080)
Globals.WINDOW_WIDTH, Globals.WINDOW_HEIGHT = info_object.current_w, info_object.current_h
Globals.WINDOW = pyg.display.set_mode((Globals.WINDOW_WIDTH, Globals.WINDOW_HEIGHT))
pyg.display.set_caption("Sprite Adventure")
os.system("cls")

# Read player data
with open(FilePaths.player, "r") as file:
    Globals.player_data = json.load(file)

# Setting up scenes
main_menu = MainMenu()
finish_menu = FinishMenu()
settings_menu = SettingsMenu()
editor = Editor()
world = World(settings_menu)

# Get number of levels available
_, _, files = next(os.walk("./data/world0/levels"))
world.max_levels = len(files)
editor.max_levels = len(files)

profiler = Profiler(Globals.FPS, (Globals.WIDTH - 25, 5), Fonts.font_20, Colors.white, display=True)

# Game loop
def control():
    global editor, main_menu, settings_menu, world, finish_menu
    current_menu = main_menu

    while True:
        profiler.update()
        response = None
        
        for event in pyg.event.get():
            Globals.mouse_position[0] = pyg.mouse.get_pos()[0] * (Globals.WIDTH / Globals.WINDOW_WIDTH)
            Globals.mouse_position[1] = pyg.mouse.get_pos()[1] * (Globals.HEIGHT / Globals.WINDOW_HEIGHT)

            if event.type == pyg.QUIT:
                quit()

            elif event.type == pyg.KEYDOWN:
                response = current_menu.keydown_event(event.key)

            elif event.type == pyg.KEYUP:
                response = current_menu.keyup_event(event.key)

            elif event.type == pyg.MOUSEBUTTONDOWN:
                response = current_menu.mousedown_event(event.button)

            elif event.type == pyg.MOUSEBUTTONUP:
                current_menu.mouseup_event(event.button)

        if current_menu.finished:
            quit()

        if current_menu.settings_active:
            current_menu.settings_active = False
            settings_menu.active = not settings_menu.active
            current_menu.overlay_active = not current_menu.overlay_active
            settings_menu.transition = (30 if settings_menu.active else -30)

        if response is not None:
            if response == "New Game":
                Globals.player_data = {
                    "current_world": 0,
                    "current_level": 0,
                    "playticks": 0,
                    "deaths": 0,
                    "times": [0, 0, 0, 0, 0]
                }
                current_menu = world
                world.load_level(world.current_world, world.current_level)

            elif response == "Continue Game":
                current_menu = world
                world.current_world = Globals.player_data["current_world"]
                world.current_level = Globals.player_data["current_level"]
                world.load_level(world.current_world, world.current_level)


            elif response == "Editor":
                current_menu = editor
                pyg.display.set_caption("Sprite Adventure - Editor")

            elif response == "Settings" and current_menu == main_menu:
                current_menu = settings_menu

            elif response == "Main Menu":
                current_menu = main_menu
                settings_menu.active = False

            elif isinstance(response, int) and current_menu == editor:
                current_menu = world
                world.current_level = editor.current_level
                world.current_world = editor.current_world
                world.load_level(0, response)
                
            elif isinstance(response, int) and current_menu == world:
                current_menu = editor
                editor.current_level = world.current_level
                editor.current_world = world.current_world
                editor.tilemap.load(f"./data/world{editor.current_world}/levels/{editor.current_level}.json")

        # Update screen
        if current_menu.update() == "Finish":
            current_menu = finish_menu
        current_menu.render()

        Globals.VID_BUFFER.blit(pyg.transform.scale(current_menu._display, (Globals.WIDTH, Globals.HEIGHT)), (0, 0))
        
        # Draw level info
        if current_menu == world:
            Globals.VID_BUFFER.blit(Fonts.font_20.render("Level: " + str(world.current_world + 1) + "-" + str(world.current_level + 1), True, Colors.white), (2, 2))
            Globals.VID_BUFFER.blit(Fonts.font_20.render("Coins: " + str(Globals.coins_collected), True, Colors.white), (2, 22))

            # Timer
            if settings_menu.data["show_timer"]:
                seconds = Globals.player_data["playticks"] / 60
                minutes = seconds // 60
                hours = minutes // 60
                playtime = ""

                # Format string
                playtime += (str(int(hours)) + ":") if hours > 0 else ""
                playtime += ("0" if minutes % 60 < 10 else "") + str(int(minutes) % 60) + ":"
                playtime += ("0" if seconds % 60 < 10 else "") + str(round(seconds % 60, 2))
                
                Globals.VID_BUFFER.blit(Fonts.font_20.render("Timer: " + playtime, True, Colors.white), (2, 44))
            
        elif current_menu == editor:
            Globals.VID_BUFFER.blit(Fonts.font_20.render("Level: " + str(editor.current_world + 1) + "-" + str(editor.current_level + 1), True, Colors.white), (2, 2))

        # Transition for settings menu
        if settings_menu.transition:
            if settings_menu.transition > 0:
                Globals.VID_BUFFER.blit(settings_menu._display, (0,  (30 - settings_menu.transition) * (Globals.HEIGHT / 30) - Globals.HEIGHT))
            else:
                Globals.VID_BUFFER.blit(settings_menu._display, (0, -(settings_menu.transition) * (Globals.HEIGHT / 30) - Globals.HEIGHT))
            
            settings_menu.transition -= abs(settings_menu.transition) // settings_menu.transition
        elif settings_menu.active:
            Globals.VID_BUFFER.blit(settings_menu._display, (0, 0))

        if settings_menu.active or settings_menu.transition:
            settings_menu.render()

        if settings_menu.data["show_fps"]:
            profiler.render(Globals.VID_BUFFER)
        
        Globals.WINDOW.blit(pyg.transform.scale(Globals.VID_BUFFER, (Globals.WINDOW_WIDTH, Globals.WINDOW_HEIGHT)), (0, 0))

        pyg.display.update()

        Globals.clock.tick(Globals.FPS)
        if current_menu == world and not world.transition:
            Globals.player_data["playticks"] += 1

def quit():
    global editor, main_menu, settings_menu, world
    settings_menu.save()
    
    # Save player data
    with open(FilePaths.player, "w") as file:
        file.write(json.dumps(Globals.player_data, indent=4))

    pyg.quit()
    sys.exit()

if __name__ == "__main__":
    control()