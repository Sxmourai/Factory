"""Getting time"""
from time import time 
import pygame
import pygame_gui
from pygame_gui.core import IncrementalThreadedResourceLoader

from src.main.camera import Camera
from src.world.world import Map
from src.ressources import load, set_game, path, TILE_IMG_HOVER
from src.menus.gui import ConstructMenu
from src.world.buildings import Factory, Core, Building
from src.menus.menu import Commands, Stats

class Game:
    """Game object"""
    PLAYER_SIZE = (30,30)
    PLAYER_IMAGE = load("player.png", PLAYER_SIZE)
    def __init__(self, size, screen_size, ticks:int=None):
        set_game(self)
        self.manager = pygame_gui.UIManager(screen_size, path("data/themes/theme.json"), resource_loader=IncrementalThreadedResourceLoader())
        self.clock = (pygame.time.Clock(), ticks)
        self.surf = pygame.display.set_mode(screen_size)
        self.camera = Camera((0,0))
        self.map = Map(size)
        self.guis  = {}
        self.texts = {}
        self.buttons = []
        self.construct_img = TILE_IMG_HOVER
        self._construct = None
        self._life = time()
        self._tick = 0
        self.stats = Stats()
        self.commands = Commands()
        self._multiplier = 1
        ConstructMenu()

    @property
    def multiplier(self):
        return self._multiplier
    @multiplier.setter
    def multiplier(self, new_multiplier):
        self._multiplier = new_multiplier

    def construct(self, pos:tuple[int,int]=None, building:Building=None) -> bool:
        """Construct a building at a position
        Args:
            pos (tuple[int]|None): Position in tiles of the building. Defaults to position of cursor (in tiles).
            building (Building, optional): Build object, to construct. Defaults to self._construct (selected by user).
        Returns:
            bool: if it could construct the building
        """
        if not isinstance(pos, tuple):
            pos = self.map.tile_from_screen(rround=True)
        if building:
            building.construct(pos)
        elif self._construct:
            self._construct(pos)
        else:return False
        return True

    def construct_overlay(self, building:Building|pygame.Surface):
        """Draws a "hollow" of the building the user is trying to construct
        Args:
            building (Building): Building to draw. Defaults to None.
        """
        if isinstance(building, pygame.Surface):
            self.construct_img = TILE_IMG_HOVER
            self._construct = None
        else:
            self.construct_img = building.hollow_img
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
            self.camera.render_text_rect(text, text_rect)
        self.manager.update(self.clock[0].tick(self.clock[1])/1000.0)
        self.manager.draw_ui(self.surf)
        pygame.display.flip()

    def screen_center(self) -> tuple[int|float]:
        """Returns a tuple with the coords of the screen's center
        Returns:
            tuple[int|float]: Coordinates of screen center
        """
        return (self.surf.get_width()/2, self.surf.get_height()/2)

    def handle_keys(self, keys):
        """Handle keys for the game (player movement etc)
        Args:
            keys (dict): Keys pressed by player
        """
        if keys:
            if keys[pygame.K_UP]:
                self.camera.move(180, keys[pygame.K_SPACE])
            if keys[pygame.K_DOWN]:
                self.camera.move(0, keys[pygame.K_SPACE])
            if keys[pygame.K_RIGHT]:
                self.camera.move(90, keys[pygame.K_SPACE])
            if keys[pygame.K_LEFT]:
                self.camera.move(270, keys[pygame.K_SPACE])
            if keys[pygame.K_f]:
                self.construct_overlay(Factory)
            if keys[pygame.K_c]:
                self.construct_overlay(Core)
            if keys[pygame.K_ESCAPE]:
                if self.construct_img == TILE_IMG_HOVER:
                    self.guis = {}
                else:
                    self.construct_overlay(TILE_IMG_HOVER)

    def handle_events(self, events) -> bool:
        """Handle pygame's events"""
        for event in events:
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONUP:
                self.click(pygame.mouse.get_pos())
            elif event.type == pygame.MOUSEMOTION:
                self.hover(pygame.mouse.get_pos())
            elif event.type == pygame_gui.UI_BUTTON_PRESSED:
                self.commands.handle_event(event)
            self.manager.process_events(event)
        return True
    def add_button(self, order, size):
        """Adds a button to game"""
        self.buttons.append(Button("button.png", order, size, self.map))

    def click(self, mpos:tuple[int,int]):
        """Handles the click of user"""
        pos = self.map.tile_from_screen(mpos, rround=True)
        build = self.map.get(pos)
        
        if build:
            if pos in self.guis:
                self.guis = {}
            else:
                self.guis = {}
                self.guis[pos] = build.gui()
        else:
            self.handle_construct()
            for gui in self.guis.values():
                gui_clicked = gui.handleClick(mpos)
                if not gui_clicked:
                    self.guis = {}
    def hover(self, mpos:tuple[int,int]):
        """Handles hover of the user"""
        for button in self.buttons:
            button.handle_hover(mpos)
            
    def factory(self,pos:tuple[int,int], tier:int) -> Factory:
        """Creates a new factory"""
        return Factory(pos, tier)
    def core(self,pos:tuple[int,int]) -> Core:
        """Creates a core"""
        return Core(pos)
    def buyable(self, price:float|int, buy_possible:bool=False):
        """Check if something is buyable, and is buy_possible=True, removes the price from points"""
        if self.stats.points >= price:
            if buy_possible:
                self.stats.points -= price
            return True
        return False
