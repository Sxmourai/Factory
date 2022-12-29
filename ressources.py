from math import sin, cos, radians
import pygame
from typing import Optional, Union
from time import time
from pathlib import Path

SCREEN_SIZE = (1000,800)

_game = []
def set_game(game):
    _game.clear()
    _game.append(game)

get_game = lambda: _game[0]
get_map = lambda: _game[0].map
get_surf = lambda: _game[0].surf

surf_width = lambda: SCREEN_SIZE[0]
surf_height = lambda: SCREEN_SIZE[1]

sysFont = lambda size: pygame.font.Font(None,size)
PATH = str(Path(".").cwd())+"\\"
path = lambda path: PATH+path
imgpath = lambda path: PATH+"img\\"+path
sc_center = lambda: (SCREEN_SIZE[0]/2, SCREEN_SIZE[1]/2)

def all(array, val, empty=True):
    if len(array) == 0:return empty
    for value in array:
        if value != val: return False
    return True

def transform(size:Union[tuple, int, float], transformer:(Optional[Union[int, float]])=None):
    """Function to center elements
    Args:
        size (Union[tuple, int, float]): Takes a size or int if only one parameter
        transformer (Optional[Union[int, float]], optional): The value to remove to size divided by 2. Defaults to None.

    Returns:
        _type_: int/float if size/float int or tuple if size tuple
    """
    if type(size) in (int,float):
        if transformer != None:
            return size - transformer/2
        else:
            return size - size/2
    return (dim - dim/2 for dim in size)

def rprint(*args, fill:bool=False, **kwargs):
    """Print with \r

    Args:
        fill (bool, optional): Adds 10 spaces-length to have better results. Defaults to False.
    """
    if fill:
        length = 0
        for arg in args:
            length += len(arg)
        print(*args, " "*(10-length), **kwargs, end="\r")
    else:print(*args, **kwargs, end="\r")
def apply_vec(origin, hyp, orientation):
    x,y = origin
    rad = radians(orientation)
    x += sin(rad)*hyp
    y += cos(rad)*hyp
    return x, y
def get_vec(hyp, orientation):
    rad = radians(orientation)
    return sin(rad)*hyp, cos(rad)*hyp

def load(img_path, size=None, multiplier:tuple=(1,1), tile:bool=False):
    img_path = imgpath(img_path)
    img = pygame.image.load(img_path)
    if size: 
        size = size[0]*multiplier[0], size[1]*multiplier[1]
        img = pygame.transform.scale(img, size)
    if tile: 
        img = pygame.transform.scale(img, get_map().TILE_SIZE)
    return img

class Shape:
    def __init__(self, pos:tuple|None, size:tuple) -> None:
        if pos:
            self._x, self._y = pos
        self._w, self._h = size
        self._rect = pygame.Rect(*pos,*size)
        self.game = get_game()
        self.surf = self.game.surf
        self.camera = self.game.camera
        self.map = self.game.map
    @property
    def x(self):
        return self._x
    @x.setter
    def x(self, x):
        self._x = x
        
    @property
    def y(self):
        return self._y
    @y.setter
    def y(self, y):
        self._y = y
        
    @property
    def w(self):
        return self._w
    @w.setter
    def w(self, w):
        self._w = w
        
    @property
    def h(self):
        return self._h
    @h.setter
    def h(self, h):
        self._h = h
        
    @property
    def pos(self):
        return (self._x,self._y)
    @pos.setter
    def pos(self, pos):
        self.rect.x,self.rect.y = pos
        self._x, self._y = pos
        
    @property
    def size(self):
        return (self._w,self._h)
    @size.setter
    def size(self, size):
        if size != self.size: 
            self.img = pygame.transform.scale(self.img, size)
            self.rect.size = size
            self._w, self._h = size
    @property
    def rect(self):
        return self._rect
    @rect.setter
    def rect(self, rect:tuple | pygame.Rect):
        if type(rect) == tuple:
            rect = pygame.Rect(*rect)
        self._rect = rect


class Sprite(Shape):
    def __init__(self, pos:tuple|None, size:tuple, imgpath):
        super().__init__(pos,size)
        self.img = load(imgpath, size)
        
    def draw_self(self):
        self.camera.render(self.img, self.rect)
