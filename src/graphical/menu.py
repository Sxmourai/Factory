import json
import pygame
from pygame_gui.elements import UITextBox, UIButton, UIPanel, UILabel, UIScrollingContainer
from pygame_gui.core import ObjectID
from pygame_gui.ui_manager import UIContainer
from os import listdir
from os.path import isfile

from src.graphical.graphical import ButtonLogo
from src.graphical.gui import ConstructMenu
from src.ressources import data, font, get_game, load, gen, surf_height, surf_width, GAME_TITLE

CONTAINER = gen(400,400)
BUTTONR = (50,50)

class Stats:
    """Stats menu"""
    def __init__(self) -> None:
        self.game = get_game()
        self.manager = self.game.manager
        self._points = 1000
        self._research = 0
        self.container = UITextBox(self.content, pygame.Rect(-2,-2, 250, 40), object_id="@stats_container")
        self.game.camera.menus.append(self)

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
        """Returns: str, the text to render stats"""
        return f"Points: {int(self._points)}  Research: {int(self._research)}"


class Commands:
    """Commands menu"""
    def __init__(self) -> None:
        self.game = get_game()
        self.manager = self.game.manager
        self.panel = UIPanel(pygame.Rect(0, 200, 40, 300), 0, self.manager, margins={"left":0,"right":0,"top":0,"bottom":0}, object_id=ObjectID("Commands", None))
        self.panel.relative_right_margin = 0
        self.panel.relative_bottom_margin = 0
        self.commands = [] # order: button
        self.construct_menu = ConstructMenu()
        self.commands.append(ButtonLogo("commands\\hammer", pygame.Rect(0,0,40,40), self.panel, object_id="@construction"))
        self.panels = []
        self.c_gui = None
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
    def handle_click_event(self, event):
        """Handle a click event for the UIButtons
        Args:
            event (_type_): Click event
        """
        for i,packer in enumerate(self.commands):
            # button, func = packer
            if event.ui_element.object_ids[-1] == "@construction": self.construct_menu.toggle()
        self.construct_menu.handle_event(event)

    def construct_panel(self):
        """Opens the construct panel"""
        if self.c_gui is None:
            self.c_gui = ConstructPan()
        elif isinstance(self.c_gui, ConstructPan):
            self.c_gui = None
    def hide(self):self.panel.hide()
    def show(self):self.panel.show()


class StartMenu:
    def __init__(self) -> None:
        self.game = get_game()
        self.manager = self.game.manager
        self.screen_rect = pygame.Rect(0,0,surf_width(),surf_height())
        container_rect = self.screen_rect.copy()
        container_rect.size = container_rect.w*.6, container_rect.h*.6
        self.container = UIPanel(container_rect,manager=self.manager, object_id="@start_panel", anchors={"center":"center"})
        self.title = UILabel(pygame.Rect(0, 10, -1, -1), GAME_TITLE, self.manager, self.container, anchors={"center":"centerx", "top":"top"}, object_id="@game_title")
        self.start = UIButton(pygame.Rect(-100,30,200,80), "Start", self.manager,self.container, "Click to start a new game", object_id="@start_button", anchors={'center': 'center'})
        self.load = UIButton(pygame.Rect(100,30,200,80), "Load", self.manager,self.container, "Click to load a game", object_id="@load_button", anchors={'center': 'center'})
        self.quit = UIButton(pygame.Rect(0,120,200,80), "Quit", self.manager,self.container, "Click to quit", object_id="@quit_button", anchors={'center': 'center'})
        self.background = load("start_background", (surf_width(), surf_height()), extension="jpg")

    def hide(self): self.container.hide()

    def draw(self):
        if self.game.started is False:
            self.game.menu_controller.commands.hide()
            self.game.surf.blit(self.background, self.screen_rect)
        else:
            self.container.hide()
            self.game.menu_controller.commands.show()
class LoadMenu:
    def __init__(self) -> None:
        self.game = get_game()
        self.manager = self.game.manager
        self.screen_rect = pygame.Rect(0,0,surf_width(),surf_height())
        container_rect = self.screen_rect.copy()
        container_rect.size = container_rect.w*.6, container_rect.h*.6
        self.container = UIPanel(container_rect,manager=self.manager, object_id="@start_panel", anchors={"center":"center"})
        self.title = UILabel(pygame.Rect(0, 10, -1, -1), GAME_TITLE, self.manager, self.container, anchors={"center":"centerx", "top":"top"}, object_id="@game_title")
        self.games = []
        self.games_container = UIScrollingContainer(pygame.Rect(0,0,container_rect.w, container_rect.h*.6),self.manager, container=self.container)
        for i,game in enumerate(self.get_games_saves()):
            self.games.append((UIButton(pygame.Rect(0, 15+55*i, 400, 50),game.title, self.manager, self.games_container, anchors={"centerx":"centerx"}), game))
        self.back = UIButton(pygame.Rect(0,-100,200,80), "Back", self.manager,self.container, "Click to go back", object_id="@back_button", anchors={'centerx': 'centerx','bottom':'bottom'})
        self.background = load("start_background", (surf_width(), surf_height()), extension="jpg")
        self.hide()
        
    def handle_click(self, event):
        for game in self.games:
            if event.ui_element == game[0]:
                self.load_game(game[1])

    def hide(self): self.container.hide()
    def show(self): self.container.show()

    def get_games_saves(self):
        for file in listdir(data("saves")):
            if file.split(".")[-1] == "json":
                with open(data("saves",file), "r") as f:
                    game = json.load(f)
                    yield GameSave(game)

    def draw(self):
        if self.game.started is False:
            self.game.menu_controller.commands.hide()
            self.game.surf.blit(self.background, self.screen_rect)
        else:
            self.container.hide()
            self.game.menu_controller.commands.show()

    def load_game(self, game):
        self.game.map.load_map(game.map)
        self.game.menu_controller.stats.points = game.stats[0]
        self.game.menu_controller.stats.research = game.stats[1]
        self.game.start()


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

class GameSave:
    def __init__(self, save) -> None:
        self.title = save["title"]
        self.map = save["map"]
        self.date = save["creationDate"]
        self.stats = save["stats"]
    @staticmethod
    def create(title, world, stats, date_of_creation):
        return GameSave({"title":title, "map":world, "stats":stats, "creationDate":date_of_creation})


class ConstructPan(Panel):
    """Derived panel"""
    def __init__(self):
        super().__init__("guis/construct", "Construct")




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
