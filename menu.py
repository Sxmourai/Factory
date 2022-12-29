from gui import Button
from typing import Optional
from ressources import Sprite,sysFont, get_game, load, surf_width, surf_height
import pygame
import pygame_gui
from pygame_gui.elements import UILabel, UITextBox, UIButton, UIPanel

gen = lambda w,h: pygame.Rect(surf_width()/2-w/2,surf_height()/2-h/2, w, h)
CONTAINER = gen(400,400)
BUTTONR = (50,50)

class Stats:
    def __init__(self) -> None:
        self.game = get_game()
        self.manager = self.game.manager
        self._points = 10
        self._research = 0
        self.container = UITextBox(self.content, pygame.Rect(-9,-9, 250, 40))

    def set_research(self, amount:int|float):
        self._research = amount
        self.container.set_text(self.content)
    def set_points(self, amount:int|float):
        self._points = amount
        self.container.set_text(self.content)
    @property
    def content(self):
        return f"Points: {int(self._points)}  Research: {int(self._research)}"


class Commands:
    def __init__(self) -> None:
        self.game = get_game()
        self.manager = self.game.manager
        self.panel = UIPanel(pygame.Rect(0, 200, 40, 300), 0, self.manager)
        self.panel.relative_right_margin = 0
        self.panel.relative_bottom_margin = 0
        self.commands = {} # order: button
        self.add_button("hammer.png", self.construct_panel)
        self.panels = []
        self.c_gui = None
    def add_button(self, imgpath:str, func):
        button = UIButton(pygame.Rect(0,0,40,40), "", self.manager, self.panel)
        self.commands[len(self.commands)+1] = (button, func)
        return button
    def handleEvent(self, e):
        for button, func in self.commands.values():
            if e.ui_element == button:
                func()
    def construct_panel(self):
        if self.c_gui == None:
            self.c_gui = Construct_pan()
        elif isinstance(self.c_gui, Construct_pan):
            self.c_gui = None


class Panel:
    def __init__(self, imgpath:str, title:str, buttons:list=[]):
        self.game = get_game()
        self.manager = self.game.manager
        self.img = load(imgpath, CONTAINER.size)
        self._text = title
        self.buttons = buttons
        self.panel = UIPanel(CONTAINER, 1, self.manager)
        self.panel.set_image(load(imgpath,CONTAINER.size))
    def button(self, text):
        button = UIButton(BUTTONR, text, self.manager, self.panel)
        self.buttons.append(button)
        return button

class Construct_pan(Panel):
    def __init__(self):
        super().__init__("guis/construct.png", "Construct", [])


# class Menu(Sprite):
#     def __init__(self, pos: tuple | None, size: tuple, imgpath):
#         super().__init__(pos, size, imgpath)
#         self.texts = {}
#         self.buttons = {}
#         self.menus = {}
#     def draw(self):
#         self.draw_self()
#         for pos, text in self.texts.items():
#             self.camera.render_text(text[0],pos, center=text[3])
#         for button in self.buttons.values():
#             button.draw()
#         for menu in self.menus.values():
#             menu.draw()


#     def add_text(self, text:str, pos:tuple, font:Optional[pygame.font.Font]=None, font_size:Optional[int]=None, color:tuple=(255,255,255), center:bool=True):
#         if font_size: font = sysFont(font_size)
#         self.texts[pos] = font.render(str(text), True, color), font, color, center
#     def change_text(self, n_text:str, pos:tuple, n_size:int=None, n_color:tuple=None, n_center:Optional[bool]=None):
#         font = sysFont(n_size) if n_size else self.texts[pos][1]
#         color = n_color if n_color else self.texts[pos][2]
#         center = n_center if n_center != None else self.texts[pos][3]
#         self.texts[pos] = font.render(str(n_text), True, color), font, color, center

#     def add_button(self,pos:tuple, *args, **kwargs):
#         self.buttons[pos] = Button(*args, **kwargs)
#     def add_menu(self,pos:tuple, size, imgpath):
#         self.menus[pos] = Menu(pos, size, imgpath)
