from ressources import load, transform,rprint
from buildings import Factory
from gui import FactoryGui
import pygame

class Map:
    SCALE = 100
    TILE_SIZE = (int(.3*SCALE), int(.3*SCALE))
    TW, TH = TILE_SIZE
    TILE_IMG = load("tile.png", TILE_SIZE)
    TILE_IMG_HOVER = load("tile_selected.png", TILE_SIZE)
    def __init__(self, size, game):
        self.size = size
        self.map = {}
        self.surf = game.surf
        self.camera = game.camera
        self.game = game
        self.last_rect = pygame.Rect(0,0,0,0)

    def set(self, pos, size, obj):
        self.map[pos] = obj
        
    def adj(self, coords):
        adj = {}
        x,y = coords
        if self.map[(x+1, y)]:
            adj['right'] = self.map[(x+1, y)]
        if self.map[(x-1, y)]:
            adj['left'] = self.map[(x-1, y)]
        if self.map[(x, y+1)]:
            adj['down'] = self.map[(x, y+1)]
        if self.map[(x, y-1)]:
            adj['up'] = self.map[(x, y-1)]
        return adj
    
    def draw(self):
        for i in range(round(self.surf.get_width()/self.TW+1)):
            for j in range(round(self.surf.get_height()/self.TH+1)):
                rect = pygame.Rect(transform(i*self.TW - self.camera.x, self.TW)+round(self.camera.x/self.TW)*self.TW, 
                                   transform(j*self.TH - self.camera.y, self.TH)+round(self.camera.y/self.TH)*self.TH, *self.TILE_SIZE)
                self.surf.blit(self.TILE_IMG, rect)
        self.camera.render(self.TILE_IMG_HOVER, self.last_rect)

        for pos, build in self.map.items():
            rect = pygame.Rect(
                transform(pos[0]*self.TW - self.camera.x,self.TW), 
                transform(pos[1]*self.TH - self.camera.y,self.TH), 
                build.w*self.TW, build.h*self.TH)
            self.surf.blit(build.img, rect)
            if type(build) is Factory:
                build.draw()

    def in_tile(self, pos,y=None, rround:bool=False):
        if type(y) in (int,float): pos = pos,y
        if rround:
            return round(pos[0]/self.TW), round(pos[1]/self.TH)
        return pos[0]/self.TW, pos[1]/self.TH
    
    def tile_from_screen(self, mpos, rround:bool=False):
        x,y = mpos
        tx,ty = self.in_tile(x+self.camera.x,y+self.camera.y, rround=rround)
        return tx,ty
        
    def pos_in_screen(self, pos):
        x,y = pos
        x = int(x/self.TW)*self.TW - (self.camera.x%self.TW)
        y = int(y/self.TH)*self.TH - (self.camera.y%self.TH)
        return x,y
    
    def click(self, mpos):
        for pos, build in self.map.items():
            if type(build) is Factory and pos == self.tile_from_screen(mpos, rround=True):
                if self.game.guis.get(pos): self.game.guis.pop(pos)
                else: self.game.guis[pos] = FactoryGui(build)
                
    def hover(self, mpos):
        tx,ty = self.tile_from_screen(mpos, rround=True)
        x,y = tx*self.TW, ty*self.TH
        x -= self.camera.x
        y -= self.camera.y
        # x -= self.camera.x%30
        # y -= self.camera.y%30
        rprint(self.camera.x%30)
        self.last_rect = pygame.Rect(x,y, *self.TILE_SIZE)
        self.last_rect.center = x,y