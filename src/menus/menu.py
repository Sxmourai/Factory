import pygame
from pygame_gui.elements import UITextBox, UIButton, UIPanel
from src.menus.gui import ConstructMenu
from src.ressources import get_game, load, gen

CONTAINER = gen(400,400)
BUTTONR = (50,50)

class Stats:
    """Stats menu"""
    def __init__(self) -> None:
        self.game = get_game()
        self.manager = self.game.manager
        self._points = 1000
        self._research = 0
        self.container = UITextBox(self.content, pygame.Rect(-9,-9, 250, 40))

    @property
    def research(self) -> int|float:
        """Returns amount of research points
        Returns:
            int: Amount of research
        """
        return self._research
    @research.setter
    def research(self, amount:int|float):
        """Sets research amount
        Args:
            amount (int | float): Amount to set to researchs
        """
        self._research = amount
        self.container.set_text(self.content)

    @property
    def points(self) -> int|float:
        """Returns amount of points"""
        return self._points
    @points.setter
    def points(self, amount:int|float):
        """Sets amount of points"""
        self._points = amount
        self.container.set_text(self.content)
    @property
    def content(self):
        """Returns:
            str: Text to render stats
        """
        return f"Points: {int(self._points)}  Research: {int(self._research)}"


class Commands:
    """Commands menu"""
    def __init__(self) -> None:
        self.game = get_game()
        self.manager = self.game.manager
        self.panel = UIPanel(pygame.Rect(0, 200, 40, 300), 0, self.manager)
        self.panel.relative_right_margin = 0
        self.panel.relative_bottom_margin = 0
        self.commands = [] # order: button
        self.add_button("hammer.png", self.construct_panel)
        self.panels = []
        self.c_gui = None
        self.construct_panell = ConstructMenu()
    def add_button(self, img_path:str, func) -> UIButton:
        """Creates a Button on the menu

        Args:
            img_path (str): Path to the logo of the button
            func (function): Function to execute on the click of the button

        Returns:
            UIButton: Button object (set into self.commands[-1][0])
        """
        if img_path:
            pass#print("Useless for now")
        button = UIButton(pygame.Rect(0,0,40,40), "", self.manager, self.panel)
        self.commands.append((button, func))
        return button
    def handle_event(self, event):
        """Handle a click event for the UIButtons

        Args:
            event (_type_): Click event
        """
        print(self.commands)
        for i,packer in enumerate(self.commands):
            button, func = packer
            func()
        self.construct_panell.handle_event(event)
        if event.ui_element == self.commands[0]:
            self.construct_panell.toggle()

    def construct_panel(self):
        """Opens the construct panel"""
        if self.c_gui is None:
            self.c_gui = ConstructPan()
        elif isinstance(self.c_gui, ConstructPan):
            self.c_gui = None


class Panel:
    """Panel object, used by the menus"""
    def __init__(self, imgpath:str, title:str):
        self.game = get_game()
        self.manager = self.game.manager
        self.img = load(imgpath, CONTAINER.size)
        self._text = title
        self.buttons = []
        self.panel = UIPanel(CONTAINER, 1, self.manager)
        self.panel.set_image(load(imgpath,CONTAINER.size))
    def button(self, text:str) -> UIButton:
        """Adds a UIButton to the panel

        Args:
            text (str): Text of the button

        Returns:
            UIButton: _description_
        """
        button = UIButton(BUTTONR, text, self.manager, self.panel)
        self.buttons.append(button)
        return button

class ConstructPan(Panel):
    """Derived panel"""
    def __init__(self):
        super().__init__("guis/construct.png", "Construct")


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
