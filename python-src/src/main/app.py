import pygame
from pygame_gui.core import IncrementalThreadedResourceLoader
from pygame_gui.ui_manager import UIManager

from src.main.event import EventController
from src.graphical.camera import Camera
from src.main.game import Game
from src.main.menu import MenuController
from src.ressources import data, set_app
from src.server.client import Client

class Application:
    def __init__(self, screen_size) -> None:
        self.buttons = []
        set_app(self)
        pygame.init()
        pygame.display.set_caption('Factory game')
        self.started = False
        self.surf = pygame.display.set_mode(screen_size)
        self.manager = UIManager(screen_size, data(
            "themes","theme.json"), resource_loader=IncrementalThreadedResourceLoader())
        self.game = Game()
        self.clock = (pygame.time.Clock(), 60)
        self.menu_controller = MenuController()
        self.event_controller = EventController()
        self.client = Client(self)

    def run(self, keys=None):
        self.draw()
        self.menu_controller.run()
        
        if keys is None: keys = pygame.key.get_pressed()
        self.event_controller.handle_keys(keys)
        return not self.event_controller.handle_events()
    
    def draw(self):
        self.game.draw()
        self.manager.update(self.clock[0].tick(self.clock[1])/1000.0)
        self.manager.draw_ui(self.surf)
        for build in self.game.map.map.values():
            build.run()
        pygame.display.flip()

    def start(self):
        if self.started is False:
            self.started = True
            self.game.start()
            self.menu_controller.start()
    def stop(self):
        if self.started is True:
            self.started = False
            self.game.stop()
            self.menu_controller.stop()
            self.game.camera.players.clear()

    def exit(self):
        if self.client.connected is True: self.client.disconnect()
        self.menu_controller.multi_menu.save_servers()
        pygame.quit()
        exit()