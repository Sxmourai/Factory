from ressources import Shape, load
import pygame
from time import time
class Sprite(Shape):
    W = 1
    H = 1
    def __init__(self, imgpath, pos, game, size=None):
        self.w, self.h = size if size else (self.W, self.H)
        super().__init__(pos, (self.w,self.h))
        self.camera = game.camera
        self.map = game.map
        self.game = game
        self.img = load(imgpath, self.size, multiplier=self.map.TILE_SIZE)
        self.map.set(pos,(self.w,self.h), self)
    def click(self):
        print("Clicked !")

class Core(Sprite):
    W,H = 2,2
    def __init__(self, pos, game):
        super().__init__("core.png", pos, game, (self.W, self.H))

class Factory(Sprite):
    W = 1
    H = 1
    def __init__(self, pos, tier, game):
        super().__init__("factory.png", pos, game, (self.W,self.H))
        self.buffer = 0
        self.max = 1000*tier
        self.gen = 1*tier
        self.edges = []
        self.balls = []
        self.last = time()
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
                
    def give(self, edge, points):
        if self.buffer - points >= 0:
            self.buffer -= points
            return edge.receive(points)
        else:
            buffer = self.buffer
            self.buffer += edge.receive(buffer)
            return points - buffer
        
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
            self.game.add_points(points)
            self.last = time()
    def draw(self):
        for ball in self.balls:
            ball.move()
class Ball(Sprite):
    height = .25
    width = .25
    def __init__(self, pos, speed, game):
        super().__init__("ball.png", pos, game, (self.width,self.height))
        self.vx, self.vy = speed
        self.x, self.y = pos
    def move(self):
        self.x += self.vx
        self.y += self.vy
