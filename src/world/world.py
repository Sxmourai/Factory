from src.ressources import load, transform,rprint, get_game, TW, TH, TILE_SIZE, TILE_IMG, TILE_IMG_HOVER

from src.world.buildings import Factory
import pygame

class Map:
    def __init__(self, size):
        self.size = size
        self.map = {}
        self.game = get_game()
        self.surf = self.game.surf
        self.camera = self.game.camera
        self.last_rect = pygame.Rect(0,0,0,0)
    def draw(self):
        for i in range(round(self.surf.get_width()/TW+1)):
            for j in range(round(self.surf.get_height()/TH+1)):
                rect = pygame.Rect(transform(i*TW - self.camera.x, TW)+round(self.camera.x/TW)*TW, 
                                   transform(j*TH - self.camera.y, TH)+round(self.camera.y/TH)*TH, *TILE_SIZE)
                self.surf.blit(TILE_IMG, rect)

        for pos, build in self.map.items():
            rect = pygame.Rect(
                pos[0]*TW - self.camera.x - TW/2,
                pos[1]*TH - self.camera.y - TH/2,
                build.w*TW, build.h*TH)
            self.camera.render(build.img, rect, transform=True)
            if type(build) is Factory:
                build.draw()
        self.hover(pygame.mouse.get_pos())
        self.camera.render(self.game.construct_img, self.last_rect)

    def in_tile(self, pos,y=None, rround:bool=False):
        if type(y) in (int,float): pos = pos,y
        if rround:
            return round(pos[0]/TW), round(pos[1]/TH)
        return pos[0]/TW, pos[1]/TH
    
    def tile_from_screen(self, mpos:tuple=(), rround:bool=False):
        if len(mpos) == 2:
            x,y = mpos
        else: x,y = pygame.mouse.get_pos()
        tx,ty = self.in_tile(x+self.camera.x,y+self.camera.y, rround=rround)
        return tx,ty
        
    def pos_in_screen(self, pos):
        x,y = pos
        x = int(x/TW)*TW - (self.camera.x%TW)
        y = int(y/TH)*TH - (self.camera.y%TH)
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
            self.hover_img = TILE_IMG_HOVER
        else:
            self.hover_img = img

    def get_from_mpos(self, mpos):
        return self.get(self.tile_from_screen(mpos, rround=True))

    def hover(self, mpos):
        tx,ty = self.tile_from_screen(mpos, rround=True)
        x,y = tx*TW, ty*TH
        x -= self.camera.x
        y -= self.camera.y
        self.last_rect = pygame.Rect(x,y, *TILE_SIZE)
        self.last_rect.center = x,y