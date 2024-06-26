# Import statements
import pygame as pyg
import json
import sys
import os

# Custom modules
from classes.display import Colors, Fonts
from classes.globals import Globals, Sounds, FilePaths
from classes.window import WindowManager

from scenes.finish_menu import FinishMenu
from scenes.main_menu import MainMenu
from scenes.settings_menu import SettingsMenu
from scenes.editor import Editor
from scenes.world import World

from utils.profiler import Profiler

window_manager = WindowManager()

# Read player data
if os.path.isfile(FilePaths.player):
    with open(FilePaths.player, "r") as file:
        Globals.player_data = json.load(file)
else:
    Globals.player_data = {
        "current_world": 0,
        "current_level": 0,
        "playticks": 0,
        "deaths": 0,
        "times": [0, 0, 0, 0, 0]
    }
    
    with open(FilePaths.player, "w") as file:
        file.write(json.dumps(Globals.player_data, indent=4))

# Setting up scenes
settings_menu = SettingsMenu()
main_menu = MainMenu()
finish_menu = FinishMenu(settings_menu)
editor = Editor()
world = World(settings_menu)

volume = settings_menu.views["sound"].sliders["sound_effects"].progress
for sound in Sounds.sfx:
    Sounds.sfx[sound].set_volume(volume)

# Get number of levels available
_, _, files = next(os.walk("./data/world0/levels"))
world.max_levels = len(files)
editor.max_levels = len(files)

profiler = Profiler(Globals.FPS, (Globals.WIDTH - 25, 5), Fonts.font_20, Colors.white, display=True)

# Game loop
def main():
    global editor, main_menu, settings_menu, world, finish_menu
    global window_manager
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
                if event.key == pyg.K_F1:
                    quit()
                elif event.key == pyg.K_F11:
                    window_manager.fullscreen()
                else:
                    response = current_menu.keydown_event(event.key)

            elif event.type == pyg.KEYUP:
                response = current_menu.keyup_event(event.key)

            elif event.type == pyg.MOUSEBUTTONDOWN:
                response = current_menu.mousedown_event(event.button)

            elif event.type == pyg.MOUSEBUTTONUP:
                current_menu.mouseup_event(event.button)

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
                world.reset()
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
                world.load_level(world.current_world, world.current_level)
                
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

            offset = 0
            if settings_menu.data["show_deaths"]:
                Globals.VID_BUFFER.blit(Fonts.font_20.render("Deaths: " + str(Globals.player_data["deaths"]), True, Colors.white), (2, 44))
                offset = 22

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
                
                Globals.VID_BUFFER.blit(Fonts.font_20.render("Timer: " + playtime, True, Colors.white), (2, 44 + offset))
            
        elif current_menu == editor:
            Globals.VID_BUFFER.blit(Fonts.font_20.render("Level: " + str(editor.current_world + 1) + "-" + str(editor.current_level + 1), True, Colors.white), (2, 2))

            if editor.show_ui:
                Globals.VID_BUFFER.blit(editor.ui_display, (0, 0))

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

        window_manager.update()

        Globals.clock.tick(Globals.FPS)
        if current_menu == world and not world.transition and not settings_menu.active:
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
    main()