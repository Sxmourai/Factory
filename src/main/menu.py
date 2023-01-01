from time import time
import pygame
from src.graphical.gui import ConstructMenu
from src.graphical.menu import Commands, LoadMenu, StartMenu, Stats, TitleScreen
from src.ressources import get_game

from pygame_gui.core import ObjectID
from pygame_gui.elements import UIButton, UILabel, UITextEntryLine, UIPanel

class MenuController:
    def __init__(self) -> None:
        self.game = get_game()
        self.manager = self.game.manager
        self.camera = self.game.camera
        self.start_menu = StartMenu(self)
        self.load_menu = LoadMenu(self)
        self.stats = Stats(self)
        self.title_screen = TitleScreen(self)
        # self.construct_menu = ConstructMenu()
        self.commands = Commands(self)
        self.dyna_menus = [self.commands.construct_menu]
        self.enabled_build_menu = None

        self.alert_container = UIPanel(pygame.Rect(0, -300, 300, 100), manager=self.manager,anchors={"center":"center"}, margins={"left":0,"right":0,"top":0,"bottom":0})
        self.alert_text = UILabel(pygame.Rect(0,0, 300,20), "", self.manager, self.alert_container,object_id="@alert_label",anchors={"centerx":"centerx"})
        self.prompt_input = UITextEntryLine(pygame.Rect(5,-36, 200, 30),self.manager,self.alert_container, anchors={"bottom":"bottom"})
        self.prompt_button = UIButton(pygame.Rect(-80,-36, 70,30),"Send",self.manager,self.alert_container, anchors={"bottom":"bottom","right":"right"},object_id="@prompt_submit")
        self.alert_container.hide()
        self.alert_time = None
        self.last_menu = self.start_menu
        self.active_menu = self.start_menu

    def run(self):
        if self.alert_time and time()-self.alert_time > 3 and not self.prompt_input.visible:
            self.alert_container.hide()
            self.alert_time = None


    @property
    def current_prompt(self):
        return self.prompt_input.get_text()

    def alert(self, text):
        self.alert_text.set_text(text)
        self.alert_container.show()
        self.prompt_input.hide()
        self.alert_time = time()

    def prompt(self, text) -> str:
        self.alert(text)
        self.prompt_input.show()


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
            elif self.title_screen.visible:
                if button_id == "@prompt_submit":
                    if self.title_screen.saving: self.game.exit(save_name=self.prompt_input.get_text())
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
            self.title_screen.save()
        elif button_id == "@back_button":
            self.last_menu.show()
            self.active_menu.hide()

    def handle_build_click(self, targeted_tile, to_construct):
        if targeted_tile:
            if self.enabled_build_menu == targeted_tile.menu:
                self.hide_building_menu()
            else:
                self.hide_building_menu()
                self.enable_building_menu(targeted_tile.menu)
        elif to_construct:
                self.enabled_build_menu = to_construct.menu
                # self.enabled_build_menu = to_construct.menu
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
