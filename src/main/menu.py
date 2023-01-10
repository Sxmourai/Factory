from time import time
import pygame
from src.graphical.gui import ConstructMenu
from src.graphical.menu import AlertContainer, Commands, LoadMenu, StartMenu, Stats, TitleScreen
from src.ressources import get_app

from pygame_gui.core import ObjectID
from pygame_gui.elements import UIButton, UILabel, UITextEntryLine, UIPanel

from src.world.buildings import Core, Factory, Generator

class MenuController:
    def __init__(self) -> None:
        self.app = get_app()
        self.game = self.app.game
        self.manager = self.app.manager
        self.camera = self.app.camera
        self.start_menu = StartMenu(self)
        self.load_menu = LoadMenu(self)
        self.stats = Stats(self)
        self.title_screen = TitleScreen(self)
        self.commands = Commands(self)
        self.alert_container = AlertContainer()
        self._menu = self.start_menu
        self._last = None
        self.statics = [self.commands, self.stats]
        for menu in self.statics:
            menu.hide()

    def run(self):
        self.alert_container.check_hiding()

    def start(self):
        self.hide_menu()
        for menu in self.statics:
            menu._show()

        buildings = [Factory, Core, Generator]
        for building in buildings:
            self.commands.construct_menu.add_building(building)

    def stop(self):self.hide_menu()
    def alert(self,text):self.alert_container.alert(text)
    def prompt(self,text):self.alert_container.prompt(text)

    def buyable(self, price:float|int, buy_possible:bool=False):
        """Check if something is buyable, and if buy_possible=True, removes the price from points"""
        if self.stats.points >= price:
            if buy_possible:
                self.stats.points -= price
            return True
        return False


    def handle_button_click_event(self, event):
        button_id = event.ui_element.object_ids[-1]
        print("menu: "+str(self.menu))
        if self.menu:
            self.menu.handle_click(button_id)
        else:
            self.handle_static_click(button_id)

    def handle_build_click(self, targeted_tile, to_construct):
        if targeted_tile:
            if self.menu == targeted_tile.menu:
                self.hide_menu()
            else:
                self.menu = targeted_tile.menu
        elif to_construct:
                self.menu = to_construct.menu
        else:
            self.hide_menu()

    def handle_static_click(self, button_id):
        for menu in self.statics:
            menu.handle_click(button_id)

    @property
    def menu(self):
        return self._menu
    @menu.setter
    def menu(self, menu):
        self._last = self.menu
        if menu:
            menu._show()
        if self._menu:
            self._menu.hide()
        self._menu = menu

    def back(self):
        self.menu.hide()
        self.menu = self._last
        self.menu._show()

    def hide_menu(self):
        self._last = self.menu
        if self.menu is not None:
            self.menu.hide()
            self.menu = None

    def hide_menus(self):
        self.hide_menu()
        for menu in self.statics:
            menu.hide()