import json
from time import time
import pygame
from pygame_gui.elements import UITextBox, UIButton, UIPanel, UILabel, UIScrollingContainer, UITextEntryLine, UIImage, UIWindow
from pygame_gui.core import ObjectID
from pygame_gui.ui_manager import UIContainer
from os import listdir
from os.path import isfile

from abc import ABC, abstractmethod


from src.graphical.player import Player
from src.graphical.graphical import ButtonLogo
from src.world.buildings import Factory,Core, Generator
# from src.graphical.gui import ConstructMenu
from src.ressources import data, font, get_app, load, gen, surf_height, surf_width, GAME_TITLE

CONTAINER = gen(400,400)
BUTTONR = (50,50)

class BasicMenu(ABC):
    def __init__(self, controller) -> None:
        self.app = get_app()
        self.game = self.app.game
        self.manager = self.app.manager
        self.controller = controller

    @property
    def visible(self): return self.container.visible
    def hide(self):self.container.hide() 
    def _show(self):self.container.show()
    def show(self):self.controller.menu = self
    def toggle(self): self.hide() if self.visible else self.show()
    def handle_click(self, button_id:str):
        if button_id == "@back_button":
            self.controller.back()
        if button_id == "@quit_button":
            self.app.exit()


class SimpleMenu(BasicMenu):
    def __init__(self, controller,static:bool=True, centered_big:bool=False) -> None:
        super().__init__(controller)
        self.static = static
        if self.static:self.game.camera.menus.append(self)
        if centered_big: self.container = UIContainer(pygame.Rect(0,0, 700, 600),self.manager, anchors={"center":"center"})


class Stats(SimpleMenu):
    """Stats menu"""
    def __init__(self, controller) -> None:
        super().__init__(controller, True)
        self._points = 1000
        self._research = 0
        self.container = UITextBox(self.content, pygame.Rect(-2,-2, 250, 40), object_id="@stats_container")



    @property
    def stats(self):
        return {"points":self.points, "research": self.research}

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


class Commands(SimpleMenu):
    """Commands menu"""
    def __init__(self,controller) -> None:
        super().__init__(controller, True)
        self.container = UIPanel(pygame.Rect(0, 200, 40, 300), 0, self.manager, margins={"left":0,"right":0,"top":0,"bottom":0}, object_id=ObjectID("Commands", None))
        self.container.relative_right_margin = 0
        self.container.relative_bottom_margin = 0
        self.commands = [] # order: button
        self.construct_menu = ConstructMenu(self.controller)
        self.add_button("commands/hammer",self.construct_menu.toggle)
        self.panels = []
        self.c_gui = None

    def add_button(self, img_path:str, func, id:str=None) -> UIButton:
        """Creates a Button on the menu

        Args:
            img_path (str): Path to the logo of the button
            func (function): Function to execute on the click of the button

        Returns:
            UIButton: Button object (set into self.commands[-1][0])
        """
        if id:
            button = ButtonLogo(img_path, pygame.Rect(0,40*len(self.commands),40,40), self.container, object_id=id)
        else:
            id = len(self.commands)
            button = ButtonLogo(img_path, pygame.Rect(0,40*len(self.commands),40,40), self.container, object_id=str(id))
        self.commands.append((button, func))
        return button

    def handle_click(self, button_id: str):
        for button,func in self.commands:
            if button_id == button.id:
                func()
                return
        self.construct_menu.handle_click(button_id)

class GlobalMenu(BasicMenu):
    def __init__(self,controller) -> None:
        super().__init__(controller)
        self.screen_rect = pygame.Rect(0,0,surf_width(),surf_height())
        container_rect = self.screen_rect.copy()
        container_rect.size = container_rect.w*.6, container_rect.h*.6
        self.container = UIPanel(container_rect,2,manager=self.manager, anchors={"center":"center"})
        self.background = UIImage(pygame.Rect(0,0,surf_width(), surf_height()),load("start_background", (surf_width(), surf_height()), extension="jpg"),self.manager)
        self.title = UILabel(pygame.Rect(0, 10, -1, -1), GAME_TITLE, self.manager, self.container, anchors={"center":"centerx", "top":"top"}, object_id="@game_title")
    def hide(self):
        super().hide()
        self.background.hide()
    def show(self):
        super().show()
        self.background.show()

class StartMenu(GlobalMenu):
    def __init__(self, controller) -> None:
        super().__init__(controller)
        self.multi = UIButton(pygame.Rect(-100,30,200,80), "Multiplayer", self.manager,self.container, "Click to connect to a server", object_id="@multi_button", anchors={'center': 'center'})
        self.load = UIButton(pygame.Rect(100,30,200,80), "Load Save", self.manager,self.container, "Click to load a game", object_id="@load_button", anchors={'center': 'center'})
        self.quit = UIButton(pygame.Rect(0,120,200,80), "Quit", self.manager,self.container, "Click to quit", object_id="@quit_button", anchors={'center': 'center'})

    def handle_click(self, button_id: str):
        super().handle_click(button_id)
        if button_id == "@multi_button":
            self.controller.multi_menu.show()
        elif button_id == "@load_button":
            self.controller.load_menu.show()

class LoadMenu(GlobalMenu):
    def __init__(self,controller) -> None:
        super().__init__(controller)
        self.games = []
        self.games_container = UIScrollingContainer(pygame.Rect(0,0,self.container.rect.w, self.container.rect.h*.6),self.manager, container=self.container)
        for i,game in enumerate(self.get_games_saves()):
            self.games.append((UIButton(pygame.Rect(0, 15+55*i, 400, 50),game.title, self.manager, self.games_container, anchors={"centerx":"centerx"}), game))
        self.back = UIButton(pygame.Rect(0,-100,200,80), "Back", self.manager,self.container, "Click to go back", object_id="@back_button", anchors={'centerx': 'centerx','bottom':'bottom'})
        self.hide()

    def show(self):
        super().show()

    def handle_click(self, button_id:str):
        super().handle_click(button_id)
        for button,game in self.games:
            if button_id == button.object_ids[-1]:
                self.load_game(game)
                break

    def get_games_saves(self):
        for file in listdir(data("saves")):
            if file.split(".")[-1] == "json":
                try:
                    with open(data("saves",file), "r") as f:
                        game = json.load(f)
                        yield GameSave(game)
                except json.decoder.JSONDecodeError:
                    print(f"Couldn't open {data('saves',file)}. The file is corrupted")

    def load_game(self, game):
        self.game.camera.player = Player((0,0), "")
        self.game.map.load_map(game.map)
        self.app.menu_controller.stats.points = game.stats["points"]
        self.app.menu_controller.stats.research = game.stats["research"]
        self.app.start()

class MultiMenu(GlobalMenu):
    def __init__(self,controller) -> None:
        super().__init__(controller)
        self.servers_button = []
        self.servers_container = UIScrollingContainer(pygame.Rect(0,0,self.container.rect.w, self.container.rect.h*.6),self.manager, container=self.container)
        self.add_server_button = UIButton(pygame.Rect(40,-175,250,60), "Add a server", self.manager,self.container, "Click to add a new server", object_id="@add_server_button", anchors={'bottom':'bottom'})
        self.add_server_popup = UIWindow(pygame.Rect(0,0,400,400),self.manager, "Add a new server", visible=False)
        self.add_server_ip = UITextEntryLine(pygame.Rect(0,30,280,50),self.manager,self.add_server_popup, anchors={"centerx":"centerx"}, placeholder_text="Ip address of the server")
        self.add_server_submit = UIButton(pygame.Rect(0,-100,300,60),"Add",self.manager,self.add_server_popup, "Click to add the server", object_id="@add_server_submit_button",anchors={"centerx":"centerx","bottom":"bottom"})

        self.back = UIButton(pygame.Rect(0,-100,200,80), "Back", self.manager,self.container, "Click to go back", object_id="@back_button", anchors={'centerx': 'centerx','bottom':'bottom'})
        self.hide()
        
        path = data("servers.json")
        try:
            with open(path, "r") as f:
                self.servers = f.read()[1:-1].split(",")
                for i in range(len(self.servers)):
                    self.servers[i] = self.servers[i][1:-1]
                
        except (json.decoder.JSONDecodeError,FileNotFoundError):
            print(f"Couldn't open {path}. The file is corrupted or deleted")
            self.servers = []
        for i,server in enumerate(self.servers):
            self.servers_button.append((UIButton(pygame.Rect(0, 15+55*i, 400, 50),server, self.manager, self.servers_container, anchors={"centerx":"centerx"},object_id=server), server))

    def save_servers(self):
        path = data("servers.json")
        with open(path, "w") as f:
            f.write(str(self.servers))


    def handle_click(self, button_id:str):
        super().handle_click(button_id)
        if button_id == self.add_server_button.object_ids[-1]:self.add_server_popup.show()
        elif button_id == self.add_server_submit.object_ids[-1]:self.add_server(self.add_server_ip.get_text());self.add_server_popup.hide()
        else:
            for button, server_ip in self.servers_button:
                if button_id == server_ip:
                    self.app.client.connect_to_server(server_ip)

    def connect_to(self, server_ip:str):
        print("Connecting to "+server_ip)

    def add_server(self, server_ip:str):
        self.servers.append(server_ip)
        self.servers_button.append((UIButton(pygame.Rect(0, 15+55*len(self.servers_button), 400, 50),server_ip, self.manager, self.servers_container, anchors={"centerx":"centerx"},object_id=server_ip), server_ip))


    def load_game(self, game):
        self.game.map.load_map(game.map)
        self.app.menu_controller.stats.points = game.stats["points"]
        self.app.menu_controller.stats.research = game.stats["research"]
        self.app.start()

class TitleScreen(GlobalMenu):
    def __init__(self,controller) -> None:
        super().__init__(controller)
        UIButton(pygame.Rect(0,0,100,100),"Hello", self.manager, self.container, "aaaa", 3)
        self.q_save = UIButton(pygame.Rect(-100,120,200,80), "Save & quit", self.manager,self.container, "Click to save & quit", object_id="@quit_save_button", anchors={'center': 'center'})
        self.q_lost = UIButton(pygame.Rect(100,120,200,80), "Quit without saving", self.manager,self.container, "Click to quit without saving", object_id="@quit_button", anchors={'center': 'center'})
        self.disconnect = UIButton(pygame.Rect(0,120,200,80), "Disconnect", self.manager,self.container, "Click to disconnect from server", object_id="@disconnect_button", anchors={'center': 'center'}, visible=False)
        self.hide()
        self.saving = False
    def show(self):
        super().show()
        if self.app.client.connected:
            self.disconnect.show()
            self.q_lost.hide()
            self.q_save.hide()
        else:
            self.disconnect.hide()
            self.q_lost.show()
            self.q_save.show()
        
    def save(self):
        self.app.menu_controller.prompt("Name of save: ")
        self.saving = True

    def handle_click(self, button_id:str):
        if button_id == "@quit_button":
            self.app.stop()
        elif button_id == "@quit_save_button":
            self.save()
            self.app.stop()
        elif button_id == "@disconnect_button":
            self.app.client.disconnect()
        else:super().handle_click(button_id)


class GameSave:
    def __init__(self, save) -> None:
        self.title = save["title"]
        self.map = save["map"]
        self.date = save["creationDate"]
        self.stats = save["stats"]
        self.raw = save
    @staticmethod
    def create(title, world, stats, date_of_creation):
        save = GameSave({"title":title, "map":world, "stats":stats, "creationDate":date_of_creation})
        save.save()
        return save
    def save(self):
        with open(data("saves", f"{self.title}.json"), "w") as f:
            json.dump(self.raw, f)


class AlertContainer(UIPanel, BasicMenu):
    def __init__(self) -> None:
        self.manager = get_app().manager
        super().__init__(pygame.Rect(0, -300, 300, 100), manager=self.manager,anchors={"center":"center"}, margins={"left":0,"right":0,"top":0,"bottom":0})
        self.text = UILabel(pygame.Rect(0,0, 300,20), "", self.manager, self,object_id="@alert_label",anchors={"centerx":"centerx"})
        self.input = UITextEntryLine(pygame.Rect(5,-36, 200, 30),self.manager,self, anchors={"bottom":"bottom"})
        self.button = UIButton(pygame.Rect(-80,-36, 70,30),"Send",self.manager,self, anchors={"bottom":"bottom","right":"right"},object_id="@prompt_submit")
        self.hide()
        self._time = None

    def alert(self, text):
        self.text.set_text(text)
        self.show()
        self.input.hide()
        self._time = time()

    def prompt(self, text) -> str:
        self.alert(text)
        self.input.show()

    def check_hiding(self):
        if self._time and time()-self._time > 3 and not self.input.visible:
            self.hide()
            self._time = None

class ConstructMenu(SimpleMenu):
    def __init__(self, controller) -> None:
        super().__init__(controller, False)
        self.container = UIPanel(pygame.Rect(0,0,surf_width()*.7,surf_height()*.7),2,self.manager, anchors={"center":"center"})
        self.buttons = []
        self.hide()

    def start(self):
        buildings = [Factory, Core, Generator]
        for building in buildings:
            self.add_building(building)

    def add_building(self, building):
        self.button(building.IMG_PATH, building.TITLE,
                    building.DESCRIPTION, self.app.event_controller.enter_construction_mode, building)

    def button(self, img_path:str|UIImage, text:str, description:str="", func=None, *args) -> int:
        p_width = self.container.rect.w
        w,h = p_width*.8,70

        rect = pygame.Rect(10,30+len(self.buttons)*h, w,h)
        container = UIContainer(rect, self.manager, container=self.container, anchors={"centerx":"centerx"})
        button_container = UIButton(pygame.Rect(0,0,*rect.size),"",self.manager,container, description, object_id=text)

        label_rect = pygame.Rect(0,5, 100, 20)
        label_rect.centerx = w/2+15

        button_container.title = UILabel(label_rect, text, self.manager, container=container)
        descr_rect = pygame.Rect(0, 20, w*.8, h-20)
        descr_rect.centerx = w/2+15
        button_container.description = UITextBox(f"<font size=2.5>{description}</font>", descr_rect, self.manager, container=container, object_id="#construct_desc")

        self.buttons.append((text, func, args))
        return button_container

    def handle_click(self, button_id):
        for bid,func,args in self.buttons:
            if button_id == bid:
                func(*args)
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

