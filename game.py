"""Getting time"""
from time import time 
import pygame
import pygame_gui
from pygame_gui.core import IncrementalThreadedResourceLoader

from camera import Camera
from world import Map
from ressources import load, transform, sysFont, all, set_game, path
from gui import Button
from buildings import Factory, Core, Building
from menu import Commands, Stats

class Game:
    """Game object"""
    PLAYER_SIZE = (30,30)
    PLAYER_IMAGE = load("player.png", PLAYER_SIZE)
    def __init__(self, size, screen_size, ticks:int=None):
        set_game(self)
        self.manager = pygame_gui.UIManager(screen_size, path("theme.json"), resource_loader=IncrementalThreadedResourceLoader())
        self.clock = (pygame.time.Clock(), ticks)
        self.surf = pygame.display.set_mode(screen_size)
        self.camera = Camera((0,0))
        self.map = Map(size)
        self.guis  = {}
        self.texts = {}
        self.buttons = []
        self.construct_img = self.map.TILE_IMG_HOVER
        self._construct = None
        self._life = time()
        self._tick = 0
        self.stats = Stats()
        self.commands = Commands()


    def construct(self, pos:tuple[int]=None, building:Building=None):
        """Construct a building at a position
        Args:
            pos (tuple[int]|None): Position in tiles of the building. Defaults to position of cursor (in tiles).
            building (Building, optional): Build object, to construct. Defaults to self._construct (selected by user).
        Returns:
            _type_: False if couldn't construct the building
        """
        pos = pos if len(pos) == 2 else self.map.tile_from_screen(rround=True)
        if building:
            building.construct(pos)
        elif self._construct:
            self._construct(pos)
        else:return False
        return True

    def construct_overlay(self, img_path_or_size:tuple[str,int] | str | pygame.Surface, building:Building=None):
        """Draws a "hollow" of the building the user is trying to construct
        Args:
            img_path_or_size (tuple[str,int] | str | pygame.Surface): Img surface or string path or tuple with path and size 
            building (Building): Building to draw. Defaults to None.
        """
        if isinstance(img_path_or_size,tuple[str,int]):
            self.construct_img = load(*img_path_or_size)
        elif isinstance(img_path_or_size,pygame.Surface):
            self.construct_img = img_path_or_size
        else:
            self.construct_img = load(img_path_or_size, self.map.TILE_SIZE)
        if self.construct_img != self.map.TILE_IMG_HOVER: self.construct_img.set_alpha(125)
        self._construct = building
        
    def handle_construct(self):
        """Handles the construction"""
        if self._construct:
            self.construct()

    def tick(self, need_set_tick:bool=True) -> int:
        """Sets the ticks elapsed since beginning of the game
        Args:
            need_set_tick (bool, optional): If the elapsed ticks should be updated. Defaults to True.

        Returns:
            _type_: Returns elapsed ticks (int)
        """
        if need_set_tick:
            self._tick = pygame.time.get_ticks()
        return self._tick

    def draw(self):
        """Draws the elements of the game (tiles, player, buildings, menus etc)"""
        self.tick()
        self.map.draw()
        self.camera.render(self.PLAYER_IMAGE, self.screen_center())
        for gui in self.guis.values():
            gui.draw()
        for button in self.buttons:
            button.draw()
        for text, text_rect in self.texts.values():
            self.camera.render_textRect(text, text_rect)
        self.manager.update(self.clock[0].tick(self.clock[1])/1000.0)
        self.manager.draw_ui(self.surf)
        pygame.display.flip()

    def screen_center(self) -> tuple[int|float]:
        """Returns a tuple with the coords of the screen's center
        Returns:
            tuple[int|float]: Coordinates of screen center
        """
        return (self.surf.get_width()/2, self.surf.get_height()/2)

    def handle_keys(self, keys:dict):
        """Handle keys for the game (player movement etc)
        Args:
            keys (dict): Keys pressed by player
        """
        if keys:
            print(type(keys), end="\r")
            if keys[pygame.K_UP]:
                self.camera.move(180, keys[pygame.K_SPACE])
            if keys[pygame.K_DOWN]:
                self.camera.move(0, keys[pygame.K_SPACE])
            if keys[pygame.K_RIGHT]:
                self.camera.move(90, keys[pygame.K_SPACE])
            if keys[pygame.K_LEFT]:
                self.camera.move(270, keys[pygame.K_SPACE])
            if keys[pygame.K_f]:
                self.construct_overlay(load("factory.png",tile=True), Factory)
            if keys[pygame.K_c]:
                self.construct_overlay(load("core.png",tile=True), Core)
            if keys[pygame.K_ESCAPE]:
                if self.construct_img == self.map.TILE_IMG_HOVER:
                    self.guis = {}
                else:
                    self.construct_overlay(self.map.TILE_IMG_HOVER)

    def handle_events(self, events) -> bool:
        for event in events:
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONUP:
                self.click(pygame.mouse.get_pos())
            elif event.type == pygame.MOUSEMOTION:
                self.hover(pygame.mouse.get_pos())
            elif event.type == pygame_gui.UI_BUTTON_PRESSED:
                self.commands.handleEvent(event)
            self.manager.process_events(event)
        return True
    @property
    def points(self):
        return self.stats._points
    @points.setter
    def points(self, points):
        self.stats.set_points(points)

    def add_button(self, order, size):
        self.buttons.append(Button("button.png", order, size, self.map))
        
    def click(self, mpos):
        pos = self.map.tile_from_screen(mpos, rround=True)
        build = self.map.get(pos)
        
        if build:
            if pos in self.guis:
                self.guis = {}
            else:
                self.guis = {}
                self.guis[pos] = build.gui()
        else:
            self.handleConstruct()
            for gui in self.guis.values():
                gui_clicked = gui.handleClick(mpos)
                if not gui_clicked:
                    self.guis = {}
    def hover(self, mpos):
        for button in self.buttons:
            button.handleHover(mpos)
            
    def factory(self,pos:tuple, tier:int):
        return Factory(pos, tier)
    def core(self,pos:tuple):
        return Core(pos)
    def buyable(self, price:float|int, buy_possible:bool=False):
        if self.points >= price:
            if buy_possible: self.points -= price
            return True
        return False