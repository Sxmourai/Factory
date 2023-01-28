"""Getting time"""
from time import time

from src.graphical.camera import Camera
from src.world.world import Map
from src.ressources import load, get_app, TILE_IMG_HOVER, sc_center, set_game
from src.graphical.menu import Commands, GameSave, Stats


class Game:
    """Game object"""
    PLAYER_SIZE = (30, 30)
    PLAYER_IMAGE = load("player", PLAYER_SIZE)

    def __init__(self):
        set_game(self)
        self.app = get_app()
        self.surf = self.app.surf
        self.manager = self.app.manager
        self.camera = Camera()
        self.map = Map()
        self._multiplier = 1
        self.started = self.app.started

    def run(self):
        self.draw()

    @property
    def multiplier(self):
        return self._multiplier

    @multiplier.setter
    def multiplier(self, new_multiplier):
        self._multiplier = new_multiplier

    def draw(self):
        """Draws the elements of the game (tiles, player, buildings, menus etc)"""
        if self.started:
            self.map.draw()
            self.camera.draw_players()

    def start(self):
        self.camera.start()
        self.started = True
    def stop(self):
        self.started = False


    def exit(self, save_name:str=None):
        if save_name:GameSave.create(save_name, self.map.unload_map(), self.menu_controller.stats.stats, time())
        self.app.stop()