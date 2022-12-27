from gui import Button
from typing import Optional
from ressources import Sprite,sysFont
import pygame

class Menu(Sprite):
    def __init__(self, pos: tuple | None, size: tuple, imgpath):
        super().__init__(pos, size, imgpath)
        self.texts = {}
        self.buttons = {}
        self.menus = {}
    def draw(self):
        self.draw_self()
        for pos, text in self.texts.items():
            self.camera.render_text(text[0],pos, center=text[3])
        for button in self.buttons.values():
            button.draw()
        for menu in self.menus.values():
            menu.draw()


    def add_text(self, text:str, pos:tuple, font:Optional[pygame.font.Font]=None, font_size:Optional[int]=None, color:tuple=(255,255,255), center:bool=True):
        if font_size: font = sysFont(font_size)
        self.texts[pos] = font.render(str(text), True, color), font, color, center
    def change_text(self, n_text:str, pos:tuple, n_size:int=None, n_color:tuple=None, n_center:Optional[bool]=None):
        font = sysFont(n_size) if n_size else self.texts[pos][1]
        color = n_color if n_color else self.texts[pos][2]
        center = n_center if n_center != None else self.texts[pos][3]
        self.texts[pos] = font.render(str(n_text), True, color), font, color, center

    def add_button(self,pos:tuple, *args, **kwargs):
        self.buttons[pos] = Button(*args, **kwargs)
    def add_menu(self,pos:tuple, size, imgpath):
        self.menus[pos] = Menu(pos, size, imgpath)