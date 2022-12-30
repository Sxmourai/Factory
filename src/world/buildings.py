from src.ressources import Shape, Sprite, load, TW, TH
from src.menus.gui import FactoryGui
import pygame
from time import time

class Building(Sprite):
    """Building on the map"""
    W = 1
    H = 1
    IMG_PATH = ""
    COST = 10
    def __init__(self, pos:tuple=()):
        super().__init__(pos, (self.W*TW, self.H*TH), self.IMG_PATH)
        if len(pos) == 2:
            self.construct(pos)
        self._gui_state = False
        self._gui = None
    def toggle_click(self):
        if self._gui_state == True: self._gui_state = False
        else: self._gui_state = True
        return self._gui_state
    def _add_gui(self, gui):
        self._gui = gui
        return gui
    def construct(self, pos=None):
        if self.game.buyable(self.COST, buy_possible=True):
            pos = pos if pos else self.pos
            self.map.set(pos, self, self.size)
            self.pos = pos
            self.constructed = True

class Core(Building):
    COST = 100
    IMG_PATH = "core.png"
    hollow_img = load(IMG_PATH, tile=True)
    hollow_img.set_alpha(125)
    def __init__(self, pos):
        super().__init__(pos)
        self.tier = 1

    # def gui(self):
    #     return super()._add_gui(CoreGui(self))

class Factory(Building):
    W,H = 1,1
    COST = 10
    IMG_PATH = "factory.png"
    hollow_img = load(IMG_PATH, tile=True)
    hollow_img.set_alpha(125)
    def __init__(self, pos, tier=1):
        super().__init__(pos)
        self.buffer = 0
        self.max = 1000*tier
        self.gen = 1*tier
        self.edges = []
        self.balls = []
        self.last = time()
        self.COST = 10*self.gen
    def gui(self):
        return super()._add_gui(FactoryGui(self))
    def output(self):
        delta = time()-self.last
        points = self.gen * delta
        if points >= 1:
            for edge in self.edges:
                points = self.give(edge, points)
                break
            if not self.edges:
                self.buffer += points
            self.last = time()

    def give(self, edge, points): #UNUSABLE
        if self.buffer - points >= 0:
            self.buffer -= points
            return edge.receive(points)
        self.buffer += edge.receive(self.buffer)
        return points - self.buffer
        
    def receive(self, points):
        if self.buffer + points > self.max:
            self.buffer = self.max
            return self.buffer+points - self.max
        self.buffer += points
        return 0
    def retrieve(self):
        delta = time()-self.last
        points = self.gen * delta
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


# class Ball(Sprite):
#     height = .25
#     width = .25
#     def __init__(self, pos, speed, game):
#         super().__init__("ball.png", pos, game, (self.width,self.height))
#         self.vx, self.vy = speed
#         self.x, self.y = pos
#     def move(self):
#         self.x += self.vx
#         self.y += self.vy



