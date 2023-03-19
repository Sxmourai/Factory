from pygame_gui import UI_BUTTON_PRESSED
from pygame_gui.elements import UIButton
import pygame
from src.graphical.menu import Stats, Commands, TitleScreen
from src.ressources import TILE_IMG_HOVER, get_app
from src.world.buildings import Building

class EventController:
    def __init__(self) -> None:
        self.app = get_app()
        self.game = self.app.game
        self.manager = self.game.manager
        self.camera = self.game.camera
        self.map = self.game.map
        self.building_menus = [] # TO FILL
        self.to_construct = None
        self.construction_mode = False


    def handle_events(self) -> bool:
        events = pygame.event.get()
        for event in events:
            self.app.manager.process_events(event)

        for event in pygame.event.get():
            if event.type == UI_BUTTON_PRESSED:
                self.app.menu_controller.handle_button_click_event(event)
                # self.game.map.handle_click(event)
                return


        for event in events:
            if event.type == pygame.QUIT:
                self.app.exit()
                return False
            elif self.app.started:
                if event.type == pygame.MOUSEBUTTONUP:
                    self.handle_click_event(event)
                elif event.type == pygame.KEYDOWN:
                    self.handle_keydown(event.key)
                elif event.type == pygame.MOUSEMOTION:
                    self.handle_hover_event(event)

    def handle_click_event(self, event):
        """Handles the click of user"""
        mpos = pygame.mouse.get_pos()
        pos = self.map.tile_from_screen(mpos, rround=True)
        
        self.app.menu_controller.handle_build_click(pos, self.to_construct)

    def handle_keydown(self, key):
        if key == pygame.K_ESCAPE:
            if self.construction_mode:
                self.exit_construction_mode()
            else:
                if self.app.menu_controller.menu not in (None, TitleScreen):
                    self.app.menu_controller.hide_menu()
                else:
                    self.app.menu_controller.title_screen.toggle()

    def handle_hover_event(self, event):
        """Handles hover of the user"""
        mpos = pygame.mouse.get_pos()



    def handle_keys(self, keys):
        """Handle keys for the game (player movement etc)
        Args:
            keys (dict): Keys pressed by player
        """
        if keys and self.app.started:
            if keys[pygame.K_UP]:
                self.camera.move(180, keys[pygame.K_SPACE])
            if keys[pygame.K_DOWN]:
                self.camera.move(0, keys[pygame.K_SPACE])
            if keys[pygame.K_RIGHT]:
                self.camera.move(90, keys[pygame.K_SPACE])
            if keys[pygame.K_LEFT]:
                self.camera.move(270, keys[pygame.K_SPACE])

    def enter_construction_mode(self, building:Building):
        pos = self.map.tile_from_screen(rround=True)
        self.to_construct = building(pos)
        self.construction_mode = True
        self.app.menu_controller.hide_menu()
    def exit_construction_mode(self):
        self.to_construct = None
        self.construction_mode = False

    def construct(self, pos):
        self.to_construct.construct(pos)
        self.enter_construction_mode(type(self.to_construct))

    @property
    def construct_img(self):
        return self.to_construct.img if self.to_construct else TILE_IMG_HOVER