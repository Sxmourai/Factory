from ressources import get_vec, sysFont, get_surf
import pygame
class Camera:
    def __init__(self, pos) -> None:
        self.x, self.y = pos
        self.surf = get_surf()
    def move(self, direction, sprint):
        speed = 3*2 if sprint else 3
        vx,vy = get_vec(speed, direction)
        self.x += vx
        self.y += vy

    def render(self, img,pos_or_rect:tuple[int]|pygame.Rect, transform:bool|tuple[bool]=False):
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

    def render_text(self, text, fontSize_or_pos:int|tuple[int], pos:tuple[int,int]=None, color:tuple[int,int,int]=(0,0,0), center:bool=True) -> tuple:
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
            if isinstance(fontSize_or_pos,tuple):
                text_rect = text.get_rect()
                pos = fontSize_or_pos
            else:
                print("Keep in mind fontSize isn't used")
                text_rect = text.get_rect()
        else:
            text = sysFont(fontSize_or_pos).render(str(text), True, color)
            text_rect = text.get_rect()
        if center:
            text_rect.center = pos
        else:
            text_rect.x, text_rect.y = pos
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
