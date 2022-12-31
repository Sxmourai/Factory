from src.graphical.gui import ConstructMenu
from src.graphical.menu import Commands, Stats
from src.ressources import get_game

class MenuController:
    def __init__(self) -> None:
        self.game = get_game()
        self.camera = self.game.camera
        self.stats = Stats()
        # self.construct_menu = ConstructMenu()
        self.commands = Commands()
        self.dyna_menus = [self.commands.construct_menu]
        self.enabled_build_menu = None

    def buyable(self, price:float|int, buy_possible:bool=False):
        """Check if something is buyable, and if buy_possible=True, removes the price from points"""
        if self.stats.points >= price:
            if buy_possible:
                self.stats.points -= price
            return True
        return False

    def handle_button_click_event(self, event):
        if self.enabled_build_menu:
            if event.ui_element == self.enabled_build_menu.retrieve:
                print("Retrieve")
        else:
            self.commands.handle_click_event(event)

    def handle_build_click(self, targeted_tile, to_construct):
        # print(build)
        if targeted_tile:
            if self.enabled_build_menu == targeted_tile.menu:
                self.hide_building_menu()
            else:
                self.hide_building_menu()
                self.enabled_build_menu = targeted_tile.menu
        elif to_construct:
                self.enabled_build_menu = to_construct.menu
        else:self.hide_building_menu()
    def hide_building_menu(self):
        if self.enabled_build_menu:
            self.enabled_build_menu.hide()

    def hide_menus(self):
        for menu in self.dyna_menus:
            menu.hide()
