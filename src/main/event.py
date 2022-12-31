from pygame_gui import UI_BUTTON_PRESSED
import pygame
from src.graphical.menu import Stats, Commands
from src.ressources import TILE_IMG_HOVER, get_game
from src.world.buildings import Building, Core, Factory

class EventController:
    def __init__(self) -> None:
        self.game = get_game()
        self.manager = self.game.manager
        self.camera = self.game.camera
        self.map = self.game.map
        self.stats = self.game.menu_controller.stats
        self.commands = self.game.menu_controller.commands
        self.building_menus = [] # TO FILL
        self.enabled_build_menu = None
        self.construct_img = TILE_IMG_HOVER
        self._construct = None


    def handle_events(self, events) -> bool:
        for event in events:
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONUP:
                self.handle_click_event(event)
            elif event.type == pygame.MOUSEMOTION:
                self.handle_hover_event(event)
            elif event.type == UI_BUTTON_PRESSED:
                self.commands.handle_event(event)
            self.manager.process_events(event)
        
            if event.type == UI_BUTTON_PRESSED:
                self.handle_button_click_event(event)
        return True

    def handle_click_event(self, event):
        """Handles the click of user"""
        mpos = pygame.mouse.get_pos()
        pos = self.map.tile_from_screen(mpos, rround=True)
        build = self.map.get(pos)

        if build:
            if self.enabled_build_menu == build.menu:
                self.hide_building_menu()
            else:
                self.hide_building_menu()
                self.enabled_build_menu = build.menu
        else:
            self.handle_construct()
            self.hide_building_menu()

    def handle_hover_event(self, event):
        """Handles hover of the user"""
        mpos = pygame.mouse.get_pos()

    def handle_button_click_event(self, event):
        if self.enabled_build_menu:
            if event.ui_element == self.enabled_build_menu.retrieve:
                print("Retrieve")


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
                    self.hide_building_menu()
                else:
                    self.construct_overlay(TILE_IMG_HOVER)

    def hide_building_menu(self):
        if self.enabled_build_menu:
            self.enabled_build_menu.hide()
            self.enabled_build_menu = None


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
