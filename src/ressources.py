from math import sin, cos, radians
from pathlib import Path
import pygame
#from time import time
GAME_TITLE = "Fusion"
PATH = str(Path(".").cwd())+"\\src\\"

SCALE = 100
TILE_SIZE = (int(.3*SCALE), int(.3*SCALE))
TW, TH = TILE_SIZE
TILE_IMG = pygame.transform.scale(pygame.image.load(PATH+"data\\img\\tile.png"), TILE_SIZE)
TILE_IMG_HOVER = pygame.transform.scale(pygame.image.load(PATH+"data\\img\\tile_selected.png"), TILE_SIZE)


SCREEN_SIZE = (1000,800)

_app = []
def set_app(app):
    _app.clear()
    _app.append(app)
_game = []
def set_game(game):
    _game.clear()
    _game.append(game)
def get_app():
    return _app[0]

get_game = lambda: _game[0]
get_map = lambda: get_game().map
get_surf = lambda: get_app().surf
get_manager = lambda: get_app().manager

surf_width = lambda: SCREEN_SIZE[0]
surf_height = lambda: SCREEN_SIZE[1]

sysFont = lambda size: pygame.font.Font(None,size)
path = lambda path: PATH+path
sc_center = lambda: (SCREEN_SIZE[0]/2, SCREEN_SIZE[1]/2)


def gen(width:int, height:int) -> pygame.Rect:
    """Creates a centered rect with width and height

    Args:
        width (int): Width of rect
        height (int): Height of rect

    Returns:
        pygame.Rect: Centered rectangle
    """
    return pygame.Rect(surf_width()/2-width/2,surf_height()/2-height/2, width, height)

def is_all(array:list|tuple, val, empty:bool=True) -> bool:
    """Check if all of the array is a certain value
    Args:
        array (list | tuple): List in question
        val (_type_): Value to check
        empty (bool, optional): Boolean value to return if the array is empty. Defaults to True.
    Returns:
        bool: True if all of the array is val else False or empty
    """
    if len(array) == 0:
        return empty
    for value in array:
        if value != val:
            return False
    return True

def transform(size:tuple[int,int]|int|float, transformer:int|float=None):
    """Function to center elements
    Args:
        size (Union[tuple, int, float]): Takes a size or int if only one parameter
        transformer (Optional[Union[int, float]], optional): The value to remove to size divided by 2. Defaults to None.

    Returns:
        _type_: int/float if size/float int or tuple if size tuple
    """
    if type(size) in (int,float):
        if transformer is not None:
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

def data(*paths):
    applied_path = PATH+"data"
    for path in paths:
        applied_path += f"\\{path}"
    return applied_path

def font(name:str, extension:str="ttf"):
    return data("font", name+"."+extension)

def imgpath(name:str, extension:str="png"):
    if extension == "":
        return data("img", name)
    return data("img", name+"."+extension)

def load(img_path:str, size:tuple[int,int]=None, multiplier:tuple[int,int]=(1,1), tile:bool=False, extension:str="png") -> pygame.Surface:
    """Loads an image

    Args:
        img_path (str): Path to the image
        size (tuple[int,int], optional): Size of the image. Defaults to None.
        multiplier (tuple[int,int], optional): Multiplier for the size. Defaults to (1,1).
        tile (bool, optional): If it's a tile (specially for Game). Defaults to False.

    Returns:
        pygame.Surface: Loaded image
    """
    treated_path = img_path.split(".")
    if len(treated_path) > 1 and treated_path[-1] != "png":
        extension = treated_path[-1]
        img_path = treated_path[0]
    img_path = imgpath(img_path, extension)
    img = pygame.image.load(img_path)
    if size:
        size = size[0]*multiplier[0], size[1]*multiplier[1]
        img = pygame.transform.scale(img, size)
    if tile:
        img = pygame.transform.scale(img, TILE_SIZE)
    return img

class Shape:
    """Shape object, with different properties"""
    def __init__(self, pos:tuple|None, size:tuple) -> None:
        if pos:
            self._x, self._y = pos
        self._w, self._h = size
        self._rect = pygame.Rect(*pos,*size)
        self.game = get_game()
        self.app = self.game.app
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
    """Shape with images"""
    def __init__(self, pos:tuple[int,int]|None, size:tuple[int,int], img_or_path:str|pygame.Surface):
        super().__init__(pos,size)
        if isinstance(img_or_path, str):
            self.img = load(img_or_path, size)
        else: self.img = img_or_path

    def draw_self(self):
        """Calls camera's render method"""
        self.camera.render(self.img, self.rect)
