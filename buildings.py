from ressources import Shape, Sprite, load, get_map
from gui import FactoryGui
import pygame
from time import time

class Building(Sprite):
    """Building on the map"""
    W = 1
    H = 1
    IMG_PATH = ""
    COST = 10
    def __init__(self, img_or_path:str|pygame.Surface, pos:tuple=()):
        super().__init__(pos, (self.W*get_map().TW, self.H*get_map().TH), img_or_path)
        self.hollow_img = self.hollow()
        if len(pos) == 2:
            self.construct(pos)
        self._gui_state = False
        self._gui = None
    def hollow(self):
        hollow_img = load(self.IMG_PATH, tile=True)
        hollow_img.set_alpha(125)
        return hollow_img
    def toggle_click(self):
        if self._gui_state == True: self._gui_state = False
        else: self._gui_state = True
        return self._gui_state
    def _add_gui(self, gui):
        self._gui = gui
        return gui
    def construct(self, pos=None):
        if self.game.buyable(self.build_cost, buy_possible=True):
            pos = pos if pos else self.pos
            self.map.set(pos, self, self.size)
            self.pos = pos
            self.constructed = True
    def to_construct(self) -> pygame.Surface:
        return self.hollow_img

class Multiblock(Shape):
    """Building larger than 1 tile"""
    def __init__(self, imgspaths:list, pos:tuple[int|str], size:tuple[int], build_type) -> None:
        """Multiblock class
        Args:
            imgspaths (list | str): Paths to the images to use. 1 ele array if only one image path
            pos (tuple[int | str]): Top left of the multiblock (IN TILE)
            size (tuple[int]): Size of multiblock (IN TILE)
        """
        # pos = pos[0]*get_map().TW, pos[1]*get_map().TH
        # size = size[0]*get_map().TW, size[1]*get_map().TH
        print("Multiblock created")
        super().__init__(pos, size)
        self.cost = 1000
        self.imgs = [load(cpath, tile=True) for cpath in imgspaths]
        self.selves = [[self.single((x,y), build_type) for y in range(self.size[1])] for x in range(self.size[0])]

    def draw(self):
        """Draws the blocks to the surface"""
        for x in self.selves:
            for selv in x:
                selv.draw()

    def find_img(self, pos_or_x:int|tuple[int,int], y:int=None) -> pygame.Surface:
        """Finds right image to a pos
        Args:
            pos_or_x (int | tuple[int]): Position in tuple or x value
            y (int, optional): Y position, optional if pos is tuple. Defaults to None.
        Returns:
            pygame.Surface: The image
        """
        if len(self.imgs) == 1:
            return None
        if y:
            x = pos_or_x
        else:x,y = pos_or_x
        return self.imgs[x][y]

    def single(self, pos:tuple[int,int], build):
        """Returns an block at the specified coordinates
        Args:
            x (int): X relative position of the block (0 for top)
            y (int): Y relative position of the block (0 for left)
        Returns:
            _type_: Block
        """
        return building_type(self.find_img(pos), self.cost/(self.w*self.h), pos)



class Core(Multiblock):
    W,H = 2,2
    COST = 100
    def __init__(self, pos):
        self.block = Building("core.png", (0,0))
        super().__init__(["core.png"], pos, (2,2), self.block)
        self.tier = 1

    # def gui(self):
    #     return super()._add_gui(CoreGui(self))

class Factory(Building):
    W,H = 1,1
    COST = 10
    IMG_PATH = "factory.png"
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
        n_points = self.game.stats.points - self.cost
        if n_points >= 0:
            self.game.stats.points = n_points
            self.gen += 1
            self.cost = 10*self.gen
            self._gui.actualise_text(new_text=f"Tier {self.gen}")
            self._gui.buttons["upgrade"].actualise_text(f"Upgrade ({self.cost})")
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



