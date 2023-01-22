from random import sample
import pygame
from src.server.parser import Parser
from src.graphical.menu import Stats
from src.graphical.player import Player
from src.ressources import get_vec, get_game, sysFont, get_surf, TW,TH

class Camera:
    """Camera object for game"""
    def __init__(self) -> None:
        self.surf = get_surf()
        self.game = None
        self.menus = []
        self.players = []
        self.player = None

    @property
    def x(self):return self.player.x
    @property
    def y(self):return self.player.y
    @property
    def tx(self):return self.x*TW
    @property
    def ty(self):return self.y*TH


    def disconnect_players(self, players:list):
        for player in players:
            print(player, "Disconnected")
            for cplayer in self.players:
                if player == cplayer.pseudo:
                    self.players.remove(cplayer)

    def move_players(self, players_moves:list):
        for player, move in players_moves:
            existing_player = False
            for cplayer in self.players:
                if player == cplayer.pseudo and cplayer != self.player:
                    cplayer.pos = move
                    existing_player = True
                    break
            if existing_player is False and player != self.player.pseudo:
                self.players.append(Player(move, player))

    def draw_players(self):
        print([player.pseudo for player in self.players], end="\r")
        for player in self.players:
            self.draw_on_tile(player.img, player.pos, (40,40), transform=True)
            
            self.render_text(player.pseudo, 10, (player.x*TW, player.y*TH-50), color=(255,255,255))
        self.surf.blit(self.player.img, pygame.Rect(self.surf.get_width()/2-self.player.w/2,self.surf.get_height()/2-self.player.h/2,self.player.w,self.player.h))

    def start(self):
        self.game = get_game()
    def move(self, direction:int|float, sprint:bool=False):
        """Moves the camera, in a direction, and if it should sprint

        Args:
            direction (int|float): Direction to move the camera (angle)
            sprint (bool): If it should sprint (double speed)
        """
        speed = .2*2 if sprint else .2
        velo_x,velo_y = get_vec(speed, direction)
        self.player.x += velo_x
        self.player.y += velo_y

    def draw_on_tile(self, img:pygame.Surface, pos_in_tile:tuple[float|int,float|int],size:tuple[float|int,float|int],transform:bool=False):
        x,y = pos_in_tile
        x *= TW
        y *= TH
        x -= self.tx
        y -= self.ty
        x += self.surf.get_width()/2
        y += self.surf.get_height()/2
        if transform:
            x -= size[0]/2
            y -= size[0]/2
        img = pygame.transform.scale(img, size)
        self.surf.blit(img, pygame.Rect(x,y, *size))

    def render(self, img:pygame.Surface,pos_or_rect:tuple[int,int]|pygame.Rect, transform:bool|tuple[bool,bool]=False):
        """Renders an image at specified coordinates or rect

        Args:
            img (pygame.Surface): Image to render
            pos_or_rect (tuple[int,int] | pygame.Rect): Position of rectangle or rect object
            transform (bool | tuple[bool,bool], optional): If it should center the image, tuple to select axis. Defaults to False.
        """
        w,h = img.get_size()
        if isinstance(pos_or_rect,tuple):
            x,y = pos_or_rect
        else:
            self.surf.blit(img, pos_or_rect)
            return
        if transform is True:
            x -= w/2
            y -= h/2
        elif isinstance(transform, tuple):
            if transform[0] is True: x -= w/2
            if transform[1] is True: y -= h/2
        self.surf.blit(img, pygame.Rect(x,y, w,h))

    def render_text(self, text,
                          font_size_or_pos:int|tuple[int],
                          pos:tuple[int,int]=None,
                          color:tuple[int,int,int]=(0,0,0),
                          transform:bool=True) -> tuple:
        """Renders text on self.surf

        Args:
            text (str): The text to display or text object (if text object, fontSize needs to be textRect)
            fontSize_textRect (int): Size of the font or textRect object if text == text object
            pos (tuple): Position of the text
            color (tuple, optional): Color of the text. Defaults to (0,0,0).

        Returns:
            tuple: returns text and his rect objects in a tuple
        """
        if isinstance(text,pygame.Surface):
            if isinstance(font_size_or_pos,tuple):
                text_rect = text.get_rect()
                pos = font_size_or_pos
            else:
                print("Keep in mind fontSize isn't used")
                text_rect = text.get_rect()
        else:
            text = sysFont(font_size_or_pos).render(str(text), True, color)
            text_rect = text.get_rect()
        
        if transform:text_rect.center = pos
        else:text_rect.x, text_rect.y = pos
        
        self.surf.blit(text, text_rect)
        return (text, text_rect)
    def render_text_rect(self, text:pygame.Surface,
                               text_rect_or_pos:pygame.Rect|tuple[int,int],
                               transform:bool=False):
        """Renders text, with a text surface and his rect or generates it

        Args:
            text (pygame.Surface): Text surface
            text_rect_or_pos (pygame.Rect | tuple[int,int]): Text rect or the position of the rect
            transform (bool, optional): If text_rect_or_pos is pos then if it should center the position of the rect. Defaults to False.
        """
        if isinstance(text_rect_or_pos, pygame.Rect):
            rect = text_rect_or_pos
        else:
            rect = pygame.Rect(*text_rect_or_pos, *text.get_size())
        if transform:
            rect.center = rect.x,rect.y
        self.surf.blit(text,rect)

    def collide(self, pos:tuple[int,int], size:tuple[int,int], point_pos:tuple[int, int], size2:tuple[int,int]=(1,1)) -> bool:
        """Checks if two points collide (first points has a size)

        Args:
            pos (tuple[int,int]): Position of the first point
            size (tuple[int,int]): Size of the first point
            point_pos (tuple[int, int]): Position of the second point
            size2 (tuple[int,int]): Size of the second point
        Returns:
            bool: If there is a collide between the points
        """
        rect1 = self.get_rect(pos, size)
        if size2 != (1,1):
            rect2 = pygame.Rect(*point_pos, *size2)
            return rect1.colliderect(rect2)
        return rect1.collidepoint(point_pos)
    def get_rect(self, pos:tuple[int,int], size:tuple[int,int], transform:bool=True) -> pygame.Rect:
        """Creates a rectangle at the position and size
        Args:
            pos (tuple[int,int]): Position of the rectangle
            size (tuple[int,int]): Size of the rectangle

        Returns:
            pygame.Rect: Created rectangle
        """
        rect = pygame.Rect(*pos, *size)
        if transform: 
            rect.center = pos
        return rect
    def center_rect(self, rect:pygame.Rect, pos:tuple[int,int]=None):
        """Center a rectangle, at specified pos, or a transformation

        Args:
            rect (pygame.Rect): Rectangle to center
            pos (tuple[int,int], optional): Position to center the rect. Defaults to his pos.
        """
        if pos:
            rect.center = pos
        else:
            rect.center = rect.x,rect.y



# class Monstre:
#     def __init__(self, position, hp, chemin_pour_texture) -> None:
#         self.pos = position
#         self.hp = hp
#         self.texture = load_texture(chemin_pour_texture)
        
#     def foo(self):
#         self.pos

# class Alien(Monstre):
#     def __init__(self, position) -> None:
#         super().__init__(position, 100, "alien.png")


# def Journée():
#     Samuser = True
#     eat(Samuser)
#     if not vacances:
#         school(False)
#     else:
#         inviterAmis(Samuser)
#     sleep(Samuser)
#     code(Samuser)
#     Journée()