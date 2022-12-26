from ressources import get_vec, sysFont
import pygame
from typing import Optional, Union
class Camera:
    def __init__(self, pos, surf) -> None:
        self.x, self.y = pos
        self.surf = surf
    def move(self, direction, sprint):
        speed = 3*2 if sprint else 3
        vx,vy = get_vec(speed, direction)
        self.x += vx
        self.y += vy
    def render(self, img,pos:tuple, size:tuple,  transform:Union[bool,tuple]=False):
        x,y = pos
        w,h = size
        if transform == True:
            x -= w/2
            y -= h/2
        elif type(transform) == tuple:
            if transform[0]==True: x -= w/2
            if transform[1]==True: y -= h/2
        self.surf.blit(img, pygame.Rect(x,y, w,h))

    def render_text(self, text, fontSize_or_pos:Union[int, tuple], pos:Optional[tuple]=None, color:tuple=(0,0,0)) -> tuple:
        """Renders text on self.surf

        Args:
            text (str): The text to display or text object (if text object, fontSize needs to be textRect)
            fontSize_textRect (int): Size of the font or textRect object if text == text object
            pos (tuple): Position of the text
            color (tuple, optional): Color of the text. Defaults to (0,0,0).

        Returns:
            tuple: returns text and his rect objects in a tuple
        """
        if type(text) is pygame.Surface:
            if type(fontSize_or_pos) is tuple:
                textRect = text.get_rect()
                pos = fontSize_or_pos
            else:
                print("Keep in mind fontSize isn't used")
                textRect = text.get_rect()
        else:
            text = sysFont(fontSize_or_pos).render(str(text), True, color)
            textRect = text.get_rect()
        textRect.center = pos
        self.surf.blit(text, textRect)
        return (text, textRect)
    def render_textRect(self, text:pygame.Surface, textRect:pygame.Rect):
        self.surf.blit(text,textRect)