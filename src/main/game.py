"""Getting time"""
from time import time 
import pygame
import pygame_gui
from pygame_gui.core import IncrementalThreadedResourceLoader

from src.graphical.camera import Camera
from src.world.world import Map
from src.ressources import load, set_game, path, TILE_IMG_HOVER, sc_center
from src.graphical.gui import ConstructMenu
from src.world.buildings import Factory, Core, Building
from src.graphical.menu import Commands, Stats
from src.main.event import EventController
from src.main.menu import MenuController

class Game:
    """Game object"""
    PLAYER_SIZE = (30,30)
    PLAYER_IMAGE = load("player.png", PLAYER_SIZE)
    def __init__(self, size, screen_size, ticks:int=None):
        set_game(self)
        self.surf = pygame.display.set_mode(screen_size)
        self.manager = pygame_gui.UIManager(screen_size, path("data/themes/theme.json"), resource_loader=IncrementalThreadedResourceLoader())
        self.clock = (pygame.time.Clock(), ticks)
        self.camera = Camera((0,0))
        self.map = Map(size)
        self._multiplier = 1
        self.menu_controller = MenuController()
        self.event_controller = EventController()

    def run(self, keys, events):
        self.draw()
        self.event_controller.handle_keys(keys)
        return self.event_controller.handle_events(events)

    @property
    def multiplier(self):
        return self._multiplier
    @multiplier.setter
    def multiplier(self, new_multiplier):
        self._multiplier = new_multiplier

    def draw(self):
        """Draws the elements of the game (tiles, player, buildings, menus etc)"""
        self.map.draw()
        self.camera.render(self.PLAYER_IMAGE, sc_center())
        # for gui in self.guis.values():
        #     gui.draw()
        self.manager.update(self.clock[0].tick(self.clock[1])/1000.0)
        self.manager.draw_ui(self.surf)
        pygame.display.flip()

    def factory(self,pos:tuple[int,int], tier:int) -> Factory:
        """Creates a new factory"""
        return Factory(pos, tier)
    def core(self,pos:tuple[int,int]) -> Core:
        """Creates a core"""
        return Core(pos)
