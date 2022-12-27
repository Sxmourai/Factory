from ressources import load, transform,rprint, get_game
from buildings import Factory
from gui import FactoryGui
import pygame

class Map:
    SCALE = 100
    TILE_SIZE = (int(.3*SCALE), int(.3*SCALE))
    TW, TH = TILE_SIZE
    TILE_IMG = load("tile.png", TILE_SIZE)
    TILE_IMG_HOVER = load("tile_selected.png", TILE_SIZE)
    def __init__(self, size):
        self.size = size
        self.map = {}
        self.game = get_game()
        self.surf = self.game.surf
        self.camera = self.game.camera
        self.last_rect = pygame.Rect(0,0,0,0)
    def draw(self):
        for i in range(round(self.surf.get_width()/self.TW+1)):
            for j in range(round(self.surf.get_height()/self.TH+1)):
                rect = pygame.Rect(transform(i*self.TW - self.camera.x, self.TW)+round(self.camera.x/self.TW)*self.TW, 
                                   transform(j*self.TH - self.camera.y, self.TH)+round(self.camera.y/self.TH)*self.TH, *self.TILE_SIZE)
                self.surf.blit(self.TILE_IMG, rect)

        for pos, build in self.map.items():
            rect = pygame.Rect(
                pos[0]*self.TW - self.camera.x - self.TW/2,
                pos[1]*self.TH - self.camera.y - self.TH/2,
                build.w*self.TW, build.h*self.TH)
            self.camera.render(build.img, rect, transform=True)
            if type(build) is Factory:
                build.draw()
        self.hover(pygame.mouse.get_pos())
        self.camera.render(self.game.construct_img, self.last_rect)

    def in_tile(self, pos,y=None, rround:bool=False):
        if type(y) in (int,float): pos = pos,y
        if rround:
            return round(pos[0]/self.TW), round(pos[1]/self.TH)
        return pos[0]/self.TW, pos[1]/self.TH
    
    def tile_from_screen(self, mpos:tuple=(), rround:bool=False):
        if len(mpos) == 2:
            x,y = mpos
        else: x,y = pygame.mouse.get_pos()
        tx,ty = self.in_tile(x+self.camera.x,y+self.camera.y, rround=rround)
        return tx,ty
        
    def pos_in_screen(self, pos):
        x,y = pos
        x = int(x/self.TW)*self.TW - (self.camera.x%self.TW)
        y = int(y/self.TH)*self.TH - (self.camera.y%self.TH)
        return x,y
    
    def get(self, index, returns=None):
        return self.map.get(index, returns)
    def pop(self, index):
        return self.map.pop(index)
    def set(self, pos, obj, size=(1,1)):
        self.map[pos] = obj
    def adj(self, coords):
        adj = {}
        x,y = coords
        if self.get((x+1, y)):
            adj['right'] = self.map[(x+1, y)]
        if self.get((x-1, y)):
            adj['left'] = self.map[(x-1, y)]
        if self.get((x, y+1)):
            adj['down'] = self.map[(x, y+1)]
        if self.get((x, y-1)):
            adj['up'] = self.map[(x, y-1)]
        return adj
    
    def select(self, img:pygame.Surface | None=None):
        if img == None:
            self.hover_img = self.TILE_IMG_HOVER
        else:
            self.hover_img = img

    def get_from_mpos(self, mpos):
        return self.get(self.tile_from_screen(mpos, rround=True))

    def hover(self, mpos):
        tx,ty = self.tile_from_screen(mpos, rround=True)
        x,y = tx*self.TW, ty*self.TH
        x -= self.camera.x
        y -= self.camera.y
        self.last_rect = pygame.Rect(x,y, *self.TILE_SIZE)
        self.last_rect.center = x,y