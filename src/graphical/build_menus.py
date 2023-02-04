import uuid
import pygame
from pygame_gui.elements import UIPanel, UIButton, UILabel
from src.ressources import *
from src.graphical.ressources import SimpleMenu

class _ConfigType(int):pass

class Config:
    NULL =   0
    INPUT =  1
    OUTPUT = 2
    ENERGY = 3
    TYPES = NULL,INPUT,OUTPUT,ENERGY
    def __init__(self, left:_ConfigType=NULL,right:_ConfigType=NULL,top:_ConfigType=NULL,bottom:_ConfigType=NULL) -> None:
        self.config = [left, right,top,bottom]
    
    @property 
    def left(self): return self.config[0]
    @property 
    def right(self): return self.config[1]
    @property 
    def top(self): return self.config[2]
    @property 
    def bottom(self): return self.config[3]

    @property
    def dict_sides(self) -> dict: return {"left":self.left, "right":self.right, "top":self.top, "bottom":self.bottom}
    
    def get(self, side:str|int):
        if isinstance(side, int): return self.config[side]
        elif isinstance(side, str): return self.dict_sides[side]
        else: print("Unknown type config index !")

    def index(self, side:str) -> int:
        match(side):
            case "left": return 0
            case "right": return 1
            case "top": return 2
            case "bottom": return 3


    @property
    def keys(self) -> tuple: return "left","right","top","bottom"
    def cycle(self, side:str|int):
        index = self.index(side)
        side_conf = self.config[index]
        if len(Config.TYPES) == side_conf+1:
            self.config[index] = Config.TYPES[0]
        else: self.config[index] = Config.TYPES[side_conf+1]

class ConfigurationMenu(UIPanel):
    def __init__(self, relative_rect: tuple[int, int]=(0,0), manager=None, *, container=None, object_id:str=None, anchors: dict[str] = None, visible: int = 1):
        size = 200
        super().__init__(pygame.Rect(*relative_rect, size, size), manager=manager, container=container, object_id=object_id, anchors=anchors, visible=visible, margins={"left":0,"right":0,"top":0,"bottom":0})
        size = 30
        self.id = uuid.uuid4()
        margin = size/2
        self.left_button = UIButton( pygame.Rect(margin,0,size, size), "", manager, self, "Click to configure left",         object_id=f"@{self.id}left_config", anchors={"centery":"centery"})
        self.right_button = UIButton(pygame.Rect(-size-margin,0,size, size), "", manager, self, "Click to configure right",  object_id=f"@{self.id}right_config", anchors={"centery":"centery", "right":"right"})
        self.top_button = UIButton(  pygame.Rect(0,margin,size, size), "", manager, self, "Click to configure top",          object_id=f"@{self.id}top_config", anchors={"centerx":"centerx"})
        self.bottom_button = UIButton( pygame.Rect(0,-size-margin,size, size), "", manager, self, "Click to configure down", object_id=f"@{self.id}down_config", anchors={"centerx":"centerx", "bottom":"bottom"})
        
        self.configs = Config()

    def handle_click(self, event_id:str):
        if event_id == self.left_button.object_ids[-1]:self.configs.cycle("left")
        elif event_id == self.right_button.object_ids[-1]:self.configs.cycle("right")
        elif event_id == self.top_button.object_ids[-1]:self.configs.cycle("top")
        elif event_id == self.bottom_button.object_ids[-1]:self.configs.cycle("bottom")


class BuildingMenu(SimpleMenu):
    def __init__(self, building, title) -> None:
        self.building = building
        self.manager = self.building.game.manager
        rect = pygame.Rect(0,0, surf_width()*.7, surf_height()*.7)
        rect.center = sc_center()
        self.container = UIPanel(rect, 1, self.manager)
        self.title = UILabel(pygame.Rect(5,5,-1,-1), title, self.manager, self.container)
        self.buttons = []
        self.hide()
    def button(self, title:str, tooltip:str="", on_click=None, *args):
        brect = pygame.Rect(0,0, 200, 50)
        brect.center = self.container.rect.w/2, self.container.rect.h/2
        brect.y -= 30
        brect.y += 60*len(self.buttons)
        button = UIButton(brect, title, self.manager, self.container, tooltip)

        self.buttons.append((button, on_click, args))
        return button
    def handle_click(self, event_id:str):
        for button,func, args in self.buttons:
            if event_id == button.object_ids[-1]:
                if callable(func):func(*args)


class StringGenMenu(BuildingMenu):
    def __init__(self, string_gen) -> None:
        super().__init__(string_gen, "String generator menu")
        self.points = UILabel(pygame.Rect(0,-100,100,50),"Buffer: 0")
        self.config = ConfigurationMenu(manager=self.manager, container=self.container, anchors={"center":"center"})
    def handle_click(self, event_id: str):
        self.config.handle_click(event_id)
        return super().handle_click(event_id)

class FactoryMenu(BuildingMenu):
    def __init__(self, factory) -> None:
        super().__init__(factory, "Factory menu")
        self.points = UILabel(pygame.Rect(0,-100,100,50),"")
        self.retrieve = self.button("Retrieve", "Click to retrieve points", factory.retrieve)
        self.upgrade = self.button("Upgrade", "Click to upgrade this factory", factory.upgrade)
