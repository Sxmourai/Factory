import json
from src.ressources import Sprite, load, TW, TH, sc_center, surf_width, surf_height
from src.graphical.build_menus import *
import pygame
from time import time

from src.world.buffer import Buffer

# Buildings defined at EOF

class Building(Sprite):
    """Building on the map"""
    W = 1
    H = 1
    COST = 10
    TITLE = "Sample"
    DESCRIPTION = "Sample building to create others"
    # if not Building in self.app.menu_controller.commands.construct_menu.BUILDINGS: self.app.menu_controller.commands.construct_menu.BUILDINGS.append(type(self))

    def __init__(self, pos:tuple[int,int], img_path:str, constructed:bool=False):
        self.buffer = Buffer(0, 200, "Sample")
        super().__init__(pos, (self.W*TW, self.H*TH), img_path)
        self.constructed = constructed
        self.menu = None
        if not self.constructed:
            self.cimg = self.img.copy()
            self.img.set_alpha(125)

    @property
    def NBT(self): return {"buffer":str(self.buffer), "pos":self.pos}
    def str(self): return self.TITLE+json.dumps(self.NBT)

    def construct(self, pos=None, buy:bool=True, send:bool=True):
        if buy:pass
        elif not self.app.menu_controller.buyable(self.COST, buy_possible=True) and self.constructed: return
        pos = pos if pos else self.pos
        self.map.set(pos, self, self.size)
        self.pos = pos
        self.img = self.cimg
        self.constructed = True
        if self.app.client.connected and send: self.app.client.construct(self)

    def run(self):
        if not self.constructed: return
        return True
    def allow_type(self, type:str):return self.buffer.allow_type(type)



class StringGenerator(Building):
    COST = 10
    DESCRIPTION = "Creates string from virtual particles. Give electricity to improve generation"
    IMG_PATH = "core"
    TRANSFER_SPEED = 1
    def __init__(self, pos: tuple[int, int], constructed: bool = False):
        super().__init__(pos, self.IMG_PATH, constructed)
        self.buffer.type = "String"
        self.tier = 1
        self.menu = StringGenMenu(self)
        self.configs = Config(self)
    def run(self):
        if super().run():
            if self.buffer < self.buffer.max:
                self.buffer += .1
            self.try_push()
            self.menu.run()
    
    def try_push(self):
        for build in self.game.map.adjacents(self.pos):
            if self.configs.allow_pushing(build.pos, self.TRANSFER_SPEED) and build.configs.allow_pulling(self.pos, self.TRANSFER_SPEED) and build.allow_type(self.buffer.type):
                if self.buffer.can_push(build.buffer, self.TRANSFER_SPEED, False): self.buffer.force_push(build.buffer, self.TRANSFER_SPEED)

class Electroliser(Building):
    COST = 10
    DESCRIPTION = "Transforms strings into electrons"
    IMG_PATH = "electroliser"
    TRANSFER_SPEED = 1
    def __init__(self, pos: tuple[int, int], constructed: bool = False):
        super().__init__(pos, self.IMG_PATH, constructed)
        self.buffer.type = "Electron"
        self.tier = 1
        self.menu = ElectroliserMenu(self)
        self.configs = Config(self)
    def run(self):
        if super().run():
            if self.buffer < self.buffer.max:
                self.buffer += .1
            self.try_push()
            self.menu.run()
    def try_push(self):
        for build in self.game.map.adjacents(self.pos):
            if self.configs.allow_pushing(build.pos, self.TRANSFER_SPEED) and build.configs.allow_pulling(self.pos, self.TRANSFER_SPEED) and build.allow_type(self.buffer.type):
                if self.buffer.can_push(build.buffer, self.TRANSFER_SPEED, False): self.buffer.force_push(build.buffer, self.TRANSFER_SPEED)

    def allow_type(self, type: str):
        if type == "String":return True


class Seller(Building):
    COST = 10
    DESCRIPTION = "Sells stuff for money $$"
    IMG_PATH = "seller"
    def __init__(self, pos: tuple[int, int], constructed: bool = False):
        super().__init__(pos, self.IMG_PATH, constructed)
        self.configs = Config(self)

    def run(self):
        if super().run():
            self.app.menu_controller.stats.points += self.buffer.int
            self.buffer.clear()

    def allow_type(self, type: str):return True

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

TITLES = {
    "String-Generator": StringGenerator,
    "Electroliser": Electroliser,
    "Seller": Seller
}
BUILDS = {} # Reversed dict

for title, build in TITLES.items():
    build.TITLE = title
    BUILDS[build] = title


BUILDINGS = TITLES.values()