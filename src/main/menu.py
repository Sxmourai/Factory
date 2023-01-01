import pygame
from src.graphical.gui import ConstructMenu
from src.graphical.menu import Commands, LoadMenu, StartMenu, Stats, TitleScreen
from src.ressources import get_game

class MenuController:
    def __init__(self) -> None:
        self.game = get_game()
        self.camera = self.game.camera
        self.start_menu = StartMenu()
        self.load_menu = LoadMenu()
        self.stats = Stats()
        self.title_screen = TitleScreen()
        # self.construct_menu = ConstructMenu()
        self.commands = Commands()
        self.dyna_menus = [self.commands.construct_menu]
        self.enabled_build_menu = None

    def active_menus(self) -> list:
        currently_active_menus = []
        if self.start_menu.visible: currently_active_menus.append(self.start_menu)
        if self.load_menu.visible: currently_active_menus.append(self.load_menu)
        for dyna_menu in self.dyna_menus:
            if dyna_menu.visible(): currently_active_menus.append(dyna_menu)
        return currently_active_menus

    def buyable(self, price:float|int, buy_possible:bool=False):
        """Check if something is buyable, and if buy_possible=True, removes the price from points"""
        if self.stats.points >= price:
            if buy_possible:
                self.stats.points -= price
            return True
        return False

    def handle_button_click_event(self, event):
        button_id = event.ui_element.object_ids[-1]
        if self.game.started:
            if self.enabled_build_menu:
                if event.ui_element in self.enabled_build_menu.buttons:
                    self.enable_building_menu.handle_click()
            else:
                self.commands.handle_click_event(event)
        else:
            if button_id == "@start_button":
                self.game.start()
            elif button_id == "@load_button":
                self.start_menu.hide()
                self.load_menu.show()
            else:self.load_menu.handle_click(event)
        
        if button_id == "@quit_button":
            self.game.exit()
        elif button_id == "@quit_save_button":
            self.game.exit(save=True)

    def handle_build_click(self, targeted_tile, to_construct):
        if targeted_tile:
            if self.enabled_build_menu == targeted_tile.menu:
                self.hide_building_menu()
            else:
                self.hide_building_menu()
                self.enable_building_menu(targeted_tile.menu)
        elif to_construct:
                self.enabled_build_menu = to_construct.menu
        else:self.hide_building_menu()

    def enable_building_menu(self, menu):
        self.enabled_build_menu = menu
        menu.show()

    def hide_building_menu(self):
        if self.enabled_build_menu:
            self.enabled_build_menu.hide()

    def hide_menus(self):
        for menu in self.dyna_menus:
            menu.hide()
        self.hide_building_menu()
        self.enabled_build_menu = None
