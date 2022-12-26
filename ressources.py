from math import sin, cos, radians
import pygame
from typing import Optional, Union
from time import time

sysFont = lambda size: pygame.font.Font(None,size)
path = lambda path: "C:\\Users\\Sxmourai\\Documents\\Projets\\Python - Factory\\img\\"+path
sc_center = lambda surf: (surf.get_width()/2, surf.get_height()/2)

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

def load(imgpath, size=None):
    imgpath = path(imgpath)
    img = pygame.image.load(imgpath)
    if size: img = pygame.transform.scale(img, size)
    return img

class Shape:
    def __init__(self, pos_or_x:Union[tuple, int,float], size_or_y:Union[tuple, int,float], width:Optional[int]=None, height:Optional[int]=None):
        if type(pos_or_x) == tuple:
            self._x, self._y = pos_or_x
            self._w, self._y = size_or_y
        else: 
            self._x,self._y = pos_or_x,size_or_y
            self._w,self._h = width,height

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
        self._x, self._y = pos
        
    @property
    def size(self):
        return (self._w,self._h)
    @size.setter
    def size(self, size):
        self._w, self._h = size
        