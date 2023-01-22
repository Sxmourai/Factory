from src.ressources import load, transform,rprint, get_game, TW, TH, TILE_SIZE, TILE_IMG, TILE_IMG_HOVER

from src.world.buildings import Core, Factory, Generator
import pygame

class Map:
    def __init__(self):
        self.map = None
        self.game = None
        self.last_rect = pygame.Rect(0,0,0,0)
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
                if type(build) is Factory:
                    build.draw()
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
        x -= self.camera.tx
        y -= self.camera.ty
        self.last_rect = pygame.Rect(x,y, *TILE_SIZE)
        self.last_rect.center = x,y

    def load_map(self, world=None):
        if not world: world = {}
        self.game = get_game()
        self.camera = self.game.camera
        self.surf = self.game.surf
        self.app = self.game.app
        self.map = {}
        for pos, build in world.items():
            pos = tuple([int(cpos) for cpos in pos.split(",")])
            if build == "Factory":
                Factory(pos).construct(buy=False)
            elif build == "Core":
                Core(pos).construct(buy=False)
            elif build == "Generator":
                Generator(pos).construct(buy=False)

    def unload_map(self) -> dict:
        unloaded_map = {}
        for pos, build in self.map.items():
            b_instance = type(build)
            if b_instance == Factory:
                b_title = "Factory"
            elif b_instance == Core:
                b_title = "Core"
            elif b_instance == Generator:
                b_title = "Generator"
            unloaded_map[f"{pos[0]},{pos[1]}"] = b_title
        return unloaded_map
    def handle_map_change(self, changes):
        if not changes:return
        print("Map changed",changes)