from ressources import Shape, Sprite, load, get_map
from gui import Gui, FactoryGui, CoreGui
import pygame
from time import time

class Building(Sprite):
    W = 1
    H = 1
    def __init__(self, imgpath, build_cost:int|float, pos:tuple=()):
        super().__init__(pos, (self.W*get_map().TW, self.H*get_map().TH), imgpath)
        self.build_cost = build_cost
        if len(pos) == 2:
            self.construct(pos)
        self._gui_state = False
        self._gui = None
    def toggle_click(self):
        if self._gui_state == True: self._gui_state = False
        else: self._gui_state = True
        return self._gui_state
    def gui(self, gui):
        self._gui = gui
        return gui
    def construct(self, pos=None):
        if self.game.buyable(self.build_cost, buy_possible=True):
            pos = pos if pos else self.pos
            self.map.set(pos, self, self.size)
            self.pos = pos
            self.constructed = True

class Multiblock(Shape):
    """Building larger than 1 tile"""
    def __init__(self, imgspaths:list, pos:tuple[int|str], size:tuple[int]) -> None:
        """Multiblock class
        Args:
            imgspaths (list | str): Paths to the images to use. 1 ele array if only one image path
            pos (tuple[int | str]): Top left of the multiblock (IN TILE)
            size (tuple[int]): Size of multiblock (IN TILE)
        """
        pos = pos[0]*get_map().TW, pos[1]*get_map().TH
        size = size[0]*get_map().TW, size[1]*get_map().TH
        super().__init__(pos, size)
        self.imgs = [load(cpath, tile=True) for cpath in imgspaths]
        self.selves = [[self.single(x,y) for y in range(self.size[1])] for x in range(self.size[0])]

    def single(self, x:int, y:int):
        """Returns an block at the specified coordinates
        Args:
            x (int): X relative position of the block (0 for top)
            y (int): Y relative position of the block (0 for left)
        Returns:
            _type_: Block
        """
        return Block(self.find_img(x,y), (x,y), self)
    def find_img(self, pos_or_x:int|tuple[int], y:int=None) -> pygame.Surface:
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
            x,y = pos_or_x,y
        else:x,y = pos_or_x
        return self.imgs[x][y]


class Block:
    """Block class for multiblocks"""
    def __init__(self, pos:tuple[int|str], multiblock:Multiblock, img_path:str=None, size:tuple[int]=(1,1)) -> None:
        self.img = load(img_path, tile=True) if img_path else None
        self.pos = pos
        self.multi = multiblock
        self.size = size
    def draw(self) -> None:
        """Draw block to surface"""
        if self.img:
            self.multi.camera.render(self.img, self.pos)



class Core(Multiblock):
    W,H = 2,2
    def __init__(self, pos):
        super().__init__(["core.png"], pos, (2,2))
        self.tier = 1

    # def gui(self):
    #     return super().gui(CoreGui(self))

class Factory(Building):
    W = 1
    H = 1
    def __init__(self, pos, tier=1):
        super().__init__("factory.png", 10, pos)
        self.buffer = 0
        self.max = 1000*tier
        self.gen = 1*tier
        self.edges = []
        self.balls = []
        self.last = time()
        self.cost = 10*self.gen
    def gui(self):
        return super().gui(FactoryGui(self))
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
            self.game.points += points
            self.last = time()
    def upgrade(self):
        n_points = self.game.points - self.cost
        if n_points >= 0:
            self.game.points = n_points
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



