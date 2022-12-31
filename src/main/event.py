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
        self.building_menus = [] # TO FILL
        self.to_construct = None
        self.construction_mode = False


    def handle_events(self, events) -> bool:
        for event in events:
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONUP:
                self.handle_click_event(event)
            elif event.type == pygame.MOUSEMOTION:
                self.handle_hover_event(event)
            elif event.type == UI_BUTTON_PRESSED:
                self.game.menu_controller.handle_button_click_event(event)
            self.manager.process_events(event)
        return True

    def handle_click_event(self, event):
        """Handles the click of user"""
        mpos = pygame.mouse.get_pos()
        pos = self.map.tile_from_screen(mpos, rround=True)
        build = self.map.get(pos)
        self.game.menu_controller.handle_build_click(build, self.to_construct)
        if build:
            if self.construction_mode: self.game.alert("Can't place that here !")
        else:
            self.construct(pos)

    def handle_hover_event(self, event):
        """Handles hover of the user"""
        mpos = pygame.mouse.get_pos()



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
                self.enter_construction_mode(Factory)
            if keys[pygame.K_c]:
                self.enter_construction_mode(Core)
            if keys[pygame.K_ESCAPE]:
                if self.construction_mode:
                    self.exit_construction_mode()
                else:
                    self.game.menu_controller.hide_building_menu()

    def enter_construction_mode(self, building:Building):
        pos = self.map.tile_from_screen(rround=True)
        self.to_construct = building(pos)
        self.construction_mode = True
        self.game.menu_controller.hide_menus()
    def exit_construction_mode(self):
        self.to_construct = None
        self.construction_mode = False

    def construct(self, pos):
        if self.construction_mode:
            self.to_construct.construct(pos)
            self.enter_construction_mode(type(self.to_construct))

    @property
    def construct_img(self):
        return self.to_construct.img if self.to_construct else TILE_IMG_HOVER
