from src.server.parser import Parser
from src.ressources import load, transform,rprint, get_game, TW, TH, TILE_SIZE, TILE_IMG, TILE_IMG_HOVER

import pygame

class Map:
    def __init__(self):
        self.map = {}
        self.game = None
        self.last_rect = pygame.Rect(0,0,0,0)
        self.camera = None
        self.surf = None
        self.app = None
    def draw(self):
        if self.game is not None:
            for i in range(round(self.surf.get_width()/TW+1)):
                for j in range(round(self.surf.get_height()/TH+1)):
                    rect = pygame.Rect(transform(i*TW - self.camera.tx, TW)+round(self.camera.tx/TW)*TW, 
                                    transform(j*TH - self.camera.ty, TH)+round(self.camera.ty/TH)*TH, *TILE_SIZE)
                    self.surf.blit(TILE_IMG, rect)

            for pos, build in self.map.items():
                rect = pygame.Rect(
                    pos[0]*TW - self.camera.tx - TW/2,
                    pos[1]*TH - self.camera.ty - TH/2,
                    build.w*TW, build.h*TH)
                self.camera.render(build.img, rect, transform=True)
            self.hover(pygame.mouse.get_pos())
            self.camera.render(self.app.event_controller.construct_img, self.last_rect)

    def in_tile(self, pos,y=None, rround:bool=False):
        if type(y) in (int,float): pos = pos,y
        if rround:
            return round(pos[0]/TW), round(pos[1]/TH)
        return pos[0]/TW, pos[1]/TH
    
    def tile_from_screen(self, mpos:tuple=(), rround:bool=False):
        if len(mpos) == 2:
            x,y = mpos
        else: x,y = pygame.mouse.get_pos()
        tx,ty = self.in_tile(x+self.camera.tx,y+self.camera.ty, rround=rround)
        return tx,ty

    def pos_in_screen(self, pos):
        x,y = pos
        x = int(x/TW)*TW - (self.camera.tx%TW)
        y = int(y/TH)*TH - (self.camera.ty%TH)
        return x,y
    
    def get(self, index, returns=None):
        return self.map.get(index, returns)
    def pop(self, index):
        return self.map.pop(index)
    def set(self, pos, obj, size=(1,1)):
        self.map[pos] = obj
    def adjacents(self, coords):
        adj = []
        x,y = coords
        if self.get((x+1, y)):
            adj.append(self.map[(x+1, y)])
        if self.get((x-1, y)):
            adj.append(self.map[(x-1, y)])
        if self.get((x, y+1)):
            adj.append(self.map[(x, y+1)])
        if self.get((x, y-1)):
            adj.append(self.map[(x, y-1)])
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
        x -= self.camera.tx
        y -= self.camera.ty
        self.last_rect = pygame.Rect(x,y, *TILE_SIZE)
        self.last_rect.center = x,y

    def load_map(self, world:dict|list=None):
        self.start()
        if not world: 
            self.game_save = None
            return
        if isinstance(world, dict):
            for pos, type,nbts in world.items():
                pos = tuple([int(cpos) for cpos in pos.split(",")])
                self.map[pos] = Parser.create_build(type, nbts)

    def unload_map(self) -> dict:
        unloaded_map = {}
        for pos, build in self.map.items():
            unloaded_map[pos] = build.str()
        return unloaded_map

    def handle_map_change(self, changes):
        if not changes:return
        for builds in changes:
            print("Type:",build_type, "nbts:",nbts)
            self.map[tuple(nbts["pos"])] = Parser.create_build(build_type, nbts)
            self.map[tuple(nbts["pos"])].construct(buy=False, send=False)
    
    def start(self):
        if self.game: 
            self.map = {}
        else:
            self.game = get_game()
            self.camera = self.game.camera
            self.surf = self.game.surf
            self.app = self.game.app
    def handle_click(self, event):
        for build in self.map.values():
            build.handle_click(event)