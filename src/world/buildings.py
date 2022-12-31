from src.ressources import Sprite, load, TW, TH, sc_center, surf_width, surf_height
# from src.graphical.gui import FactoryGui, CoreGui
import pygame
from pygame_gui.elements import UIButton, UILabel, UIImage, UIPanel
from time import time

class Building(Sprite):
    """Building on the map"""
    W = 1
    H = 1
    COST = 10
    TITLE = "Sample"
    DESCRIPTION = "Sample building to create others"
    def __init__(self, pos:tuple[int,int], img_path:str, constructed:bool=False):
        self.constructed = constructed
        super().__init__(pos, (self.W*TW, self.H*TH), img_path)
        self.menu = None
        if not self.constructed:
            self.cimg = self.img.copy()
            self.img.set_alpha(125)

    def construct(self, pos=None):
        if self.game.menu_controller.buyable(self.COST, buy_possible=True) and not self.constructed:
            pos = pos if pos else self.pos
            self.map.set(pos, self, self.size)
            self.pos = pos
            self.img = self.cimg
            self.constructed = True

class Core(Building):
    COST = 100
    TITLE = "Core"
    DESCRIPTION = "The core doesn't have a use for now... Sorry"
    IMG_PATH = "core"
    def __init__(self, pos, constructed:bool=False):
        super().__init__(pos,self.IMG_PATH, constructed)
        self.tier = 1
        self.menu = CoreMenu(self)

    # def gui(self):
    #     return super()._add_gui(CoreGui(self))

class Factory(Building):
    W,H = 1,1
    COST = 10
    TITLE = "Factory"
    DESCRIPTION = "The factory produces points that you can use in the shop."
    IMG_PATH = "factory"
    def __init__(self, pos, tier=1, constructed:bool=False):
        super().__init__(pos, self.IMG_PATH, constructed)
        self.buffer = 0
        self.max = 1000*tier
        self.gen = 1*tier
        self.edges = []
        self.balls = []
        self.last = time()
        self.COST = 10*self.gen
        self.menu = FactoryMenu(self)
    def retrieve(self):
        delta = time()-self.last
        points = self.gen * delta * self.game.multiplier
        if points >= 1:
            self.game.stats.points += points
            self.last = time()
    def upgrade(self):
        n_points = self.game.stats.points - self.COST
        if n_points >= 0:
            self.game.stats.points = n_points
            self.gen += 1
            self.COST = 10*self.gen
            self._gui.actualise_text(new_text=f"Tier {self.gen}")
            self._gui.buttons["upgrade"].actualise_text(f"Upgrade ({self.COST})")
    def draw(self):
        for ball in self.balls:
            ball.move()


class Generator(Building):
    COST = 500
    TITLE = "Generator"
    DESCRIPTION = "The generator boosts the production of the factory."
    IMG_PATH = "generator"
    def __init__(self, pos:tuple[int,int], constructed:bool=False):
        super().__init__(pos, self.IMG_PATH, constructed)
        self._tier = 1
        self.game.multiplier += self.tier
    @property
    def tier(self):
        return self._tier
    @tier.setter
    def tier(self, new_tier):
        self._tier = new_tier

class BuildingMenu:
    def __init__(self, building) -> None:
        self.building = building
        self.manager = self.building.game.manager
        rect = pygame.Rect(0,0, surf_width()*.7, surf_height()*.7)
        rect.center = sc_center()
        self.container = UIPanel(rect, 1, self.manager)
        self.hide()
    def hide(self):
        self.container.hide()
    def show(self):
        self.container.show()

class CoreMenu(BuildingMenu):
    def __init__(self, core:Core) -> None:
        super().__init__(core)
class FactoryMenu(BuildingMenu):
    def __init__(self, factory:Factory) -> None:
        super().__init__(factory)
        brect = pygame.Rect(0,0, 100, 40)
        brect.center = sc_center()
        brect.y -= 30
        self.retrieve = UIButton(brect, "Retrieve", self.manager, self.container, "Click to retrieve points")
