from src.graphical.gui import ConstructMenu
from src.graphical.menu import Commands, Stats
from src.ressources import get_game

class MenuController:
    def __init__(self) -> None:
        self.game = get_game()
        self.camera = self.game.camera
        self.stats = Stats()
        self.construct_menu = ConstructMenu()
        self.commands = Commands()
    def buyable(self, price:float|int, buy_possible:bool=False):
        """Check if something is buyable, and if buy_possible=True, removes the price from points"""
        if self.stats.points >= price:
            if buy_possible:
                self.stats.points -= price
            return True
        return False
    