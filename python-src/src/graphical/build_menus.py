import uuid
import pygame
from pygame_gui.elements import UIPanel, UIButton, UILabel
from src.ressources import *
from src.graphical.ressources import SimpleMenu

BUTTON_SIZE = 40
TILT_WIDTH = BUTTON_SIZE/6
TILT_HEIGHT = BUTTON_SIZE/3
BUTTON_PADDING = 3.5

class _ConfigType(int):pass

def conf_str(type:_ConfigType):
    if type == Config.NULL: return   "@NULL"
    if type == Config.INPUT: return  "@INPUT"
    if type == Config.OUTPUT: return "@OUTPUT"
    if type == Config.ENERGY: return "@ENERGY"

class Part:
    def __init__(self, config_menu, side:str, buffer, menu) -> None:
        self.configuration_menu = config_menu
        self.side = Config.index(side, return_int=True)
        self.str_side = Config.index(side, return_int=False)
        self.buffer = buffer
        match(self.str_side):
            case "left": rect =  pygame.Rect(BUTTON_SIZE/2,0,BUTTON_SIZE, BUTTON_SIZE)              
            case "right": rect = pygame.Rect(-BUTTON_SIZE-BUTTON_SIZE/2,0,BUTTON_SIZE, BUTTON_SIZE) 
            case "top": rect =   pygame.Rect(0,BUTTON_SIZE/2,BUTTON_SIZE, BUTTON_SIZE)              
            case "bottom": rect =pygame.Rect(0,-BUTTON_SIZE-BUTTON_SIZE/2,BUTTON_SIZE, BUTTON_SIZE) 
        self.button = UIButton(rect, "", self.configuration_menu.manager, self, "Click to configure "+self.str_side,         object_id=f"@{self.id}{self.str_side}_config", anchors={"centery":"centery"})


class Config:
    NULL =   0
    INPUT =  1
    OUTPUT = 2
    ENERGY = 3
    TYPES = NULL,INPUT,OUTPUT,ENERGY
    def __init__(self, building=None, left:_ConfigType=NULL,right:_ConfigType=NULL,top:_ConfigType=NULL,bottom:_ConfigType=NULL) -> None:
        self.config = [left, right,top,bottom]
        self.build = building
        if self.build.menu and self.build.menu.configuration_menu:
            self.build.menu.configuration_menu.left_button.object_ids[-2] = conf_str(self.left)
            self.build.menu.configuration_menu.right_button.object_ids[-2] = conf_str(self.right)
            self.build.menu.configuration_menu.top_button.object_ids[-2] = conf_str(self.top)
            self.build.menu.configuration_menu.bottom_button.object_ids[-2] = conf_str(self.bottom)

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

    def allow_pushing(self, coords:tuple[int,int], amount:int|float) -> bool:
        x,y = coords
        if self.build.x - x == 1: return self.config[0] == Config.OUTPUT # LEFT
        if self.build.x - x == -1: return self.config[1] == Config.OUTPUT # RIGHT
        if self.build.y - y == 1: return self.config[2] == Config.OUTPUT # TOP
        if self.build.y - y == -1: return self.config[3] == Config.OUTPUT # BOTTOM

    def allow_pulling(self, coords:tuple[int,int], amount:int|float, type_of_buffer=None) -> bool: # TODO
        x,y = coords
        if self.build.buffer+amount > self.build.buffer.max: return False
        if not type_of_buffer: type_of_buffer = self.build.buffer.type
        if self.build.x - x == 1:  return self.config[0] != Config.OUTPUT and self.build.buffer.type == type_of_buffer # LEFT
        if self.build.x - x == -1: return self.config[1] != Config.OUTPUT and self.build.buffer.type == type_of_buffer # RIGHT
        if self.build.y - y == 1:  return self.config[2] != Config.OUTPUT and self.build.buffer.type == type_of_buffer # TOP
        if self.build.y - y == -1: return self.config[3] != Config.OUTPUT and self.build.buffer.type == type_of_buffer # BOTTOM

    @staticmethod
    def index(side:str|int, return_int:bool=False) -> int|str:
        match(side):
            case "left":  return 0 if return_int else "left"
            case "right": return 1 if return_int else "right"
            case "top":   return 2 if return_int else "top"
            case "bottom":return 3 if return_int else "bottom"
            case 0:       return 0 if return_int else "left"
            case 1:       return 1 if return_int else "right"
            case 2:       return 2 if return_int else "top"
            case 3:       return 3 if return_int else "bottom"

    @property
    def keys(self) -> tuple: return "left","right","top","bottom"
    def cycle(self, side:str|int, reversed:bool=False):
        index = self.index(side, return_int=True)
        side_conf = self.config[index]
        # if len(Config.TYPES) == side_conf+1 and not reversed:
        #     self.config[index] = Config.TYPES[0]
        # elif side_conf > 1 and reversed: self.config[index] = Config.TYPES[side_conf-1]
        # else: self.config[index] = Config.TYPES[side_conf-1]
        if not reversed:
            if len(Config.TYPES) == side_conf+1:
                  self.config[index] = Config.TYPES[0]
            else: self.config[index] = Config.TYPES[side_conf+1] 
        else:
            if side_conf>=1:
                  self.config[index] = Config.TYPES[side_conf-1] 
            else: self.config[index] = Config.TYPES[-1]
            
        if self.build.menu: 
            self.build.menu.configuration_menu.menus[index].object_ids[-2] = conf_str(self.config[index])


class ConfigurationMenu(UIPanel):
    COLORS =[
                (100,100,100), # Config.NULL
                (255,80,80), # Config.INPUT
                (80,80,255), # Config.OUTPUT
                (255,200,100), # Config.ENERGY
            ]


    def __init__(self, build, relative_rect: tuple[int, int]=(0,0), manager=None, *, container=None, object_id:str=None, anchors: dict[str] = None, visible: int = 1):
        size = 200
        super().__init__(pygame.Rect(*relative_rect, size, size), manager=manager, container=container, object_id=object_id, anchors=anchors, visible=visible, margins={"left":0,"right":0,"top":0,"bottom":0})
        self.id = uuid.uuid4()
        margin = BUTTON_SIZE/2
        self.left_button =  UIButton(, "", manager, self, "Click to configure left",         object_id=f"@{self.id}left_config", anchors={"centery":"centery"})
        self.right_button = UIButton(, "", manager, self, "Click to configure right",  object_id=f"@{self.id}right_config", anchors={"centery":"centery", "right":"right"})
        self.top_button =   UIButton(, "", manager, self, "Click to configure top",          object_id=f"@{self.id}top_config", anchors={"centerx":"centerx"})
        self.bottom_button =UIButton(, "", manager, self, "Click to configure down", object_id=f"@{self.id}down_config", anchors={"centerx":"centerx", "bottom":"bottom"})
        self.menus = [self.left_button, self.right_button, self.top_button, self.bottom_button]
        self.build = build

    def run(self):
        if self.visible:
                rect = self.left_button.rect
                bottom_left =  rect.left+BUTTON_PADDING,rect.bottom-BUTTON_PADDING
                top_left =     rect.left+BUTTON_PADDING,rect.top+BUTTON_PADDING
                bottom_right = rect.left+BUTTON_PADDING+TILT_WIDTH, rect.bottom-BUTTON_PADDING-TILT_HEIGHT/2
                top_right =    rect.left+BUTTON_PADDING+TILT_WIDTH, rect.top+BUTTON_PADDING+TILT_HEIGHT/2
                polygon_points = bottom_left, bottom_right, top_right, top_left
                pygame.draw.polygon(get_surf(),self.COLORS[self.build.configs.config[0]],polygon_points)
                rect = self.right_button.rect
                top_right =    rect.right-BUTTON_PADDING,rect.top+BUTTON_PADDING
                bottom_right = rect.right-BUTTON_PADDING,rect.bottom-BUTTON_PADDING
                bottom_left =  rect.right-BUTTON_PADDING-TILT_WIDTH, rect.bottom-BUTTON_PADDING-TILT_HEIGHT/2
                top_left =     rect.right-BUTTON_PADDING-TILT_WIDTH, rect.top+BUTTON_PADDING+TILT_HEIGHT/2
                polygon_points = bottom_left, bottom_right, top_right, top_left
                pygame.draw.polygon(get_surf(),self.COLORS[self.build.configs.config[1]],polygon_points)
                
                rect = self.top_button.rect
                top_left =     rect.left+BUTTON_PADDING,rect.top+BUTTON_PADDING
                top_right =    rect.right-BUTTON_PADDING,rect.top+BUTTON_PADDING
                bottom_left =  rect.left+BUTTON_PADDING+TILT_WIDTH, rect.top+BUTTON_PADDING+TILT_HEIGHT
                bottom_right = rect.right-BUTTON_PADDING-TILT_WIDTH, rect.top+BUTTON_PADDING+TILT_HEIGHT
                polygon_points = bottom_left, bottom_right, top_right, top_left
                pygame.draw.polygon(get_surf(),self.COLORS[self.build.configs.config[2]],polygon_points)
                rect = self.bottom_button.rect
                bottom_left =  rect.left+BUTTON_PADDING,rect.bottom-BUTTON_PADDING
                bottom_right = rect.right-BUTTON_PADDING,rect.bottom-BUTTON_PADDING
                top_right =    rect.right-BUTTON_PADDING-TILT_WIDTH, rect.bottom-BUTTON_PADDING-TILT_HEIGHT
                top_left =     rect.left+BUTTON_PADDING+TILT_WIDTH, rect.bottom-BUTTON_PADDING-TILT_HEIGHT
                polygon_points = bottom_left, bottom_right, top_right, top_left
                pygame.draw.polygon(get_surf(),self.COLORS[self.build.configs.config[3]],polygon_points)

    def handle_click(self, event:pygame.event.Event):
        button = event.ui_element
        reversed = pygame.key.get_pressed()[pygame.K_LSHIFT]
        if button == self.left_button:self.build.configs.cycle("left", reversed=reversed)
        elif button == self.right_button:self.build.configs.cycle("right", reversed=reversed)
        elif button == self.top_button:self.build.configs.cycle("top", reversed=reversed)
        elif button == self.bottom_button:self.build.configs.cycle("bottom", reversed=reversed)


class BuildingMenu(SimpleMenu):
    def __init__(self, building, title) -> None:
        self.build = building
        self.manager = self.build.game.manager
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
        self.points = UILabel(pygame.Rect(0,50,100,50),"Buffer: 0",self.manager, self.container, anchors={"centerx":"centerx"})
        self.configuration_menu = ConfigurationMenu(self.build, manager=self.manager, container=self.container, anchors={"center":"center"})
    def handle_click(self, event_id: str):
        self.configuration_menu.handle_click(event_id)
        return super().handle_click(event_id)
    def run(self):
        self.configuration_menu.run()
        self.points.set_text("Buffer: "+str(self.build.buffer))

class ElectroliserMenu(BuildingMenu):
    def __init__(self, electroliser) -> None:
        super().__init__(electroliser, "Electroliser menu")
        self.points = UILabel(pygame.Rect(0,50,100,50),"Buffer: 0",self.manager, self.container, anchors={"centerx":"centerx"})
        self.configuration_menu = ConfigurationMenu(self.build, manager=self.manager, container=self.container, anchors={"center":"center"})
    def handle_click(self, event_id: str):
        self.configuration_menu.handle_click(event_id)
        return super().handle_click(event_id)
    def run(self):
        self.configuration_menu.run()
        self.points.set_text("Buffer: "+str(self.build.buffer))








class FactoryMenu(BuildingMenu):
    def __init__(self, factory) -> None:
        super().__init__(factory, "Factory menu")
        self.points = UILabel(pygame.Rect(0,-100,100,50),"")
        self.retrieve = self.button("Retrieve", "Click to retrieve points", factory.retrieve)
        self.upgrade = self.button("Upgrade", "Click to upgrade this factory", factory.upgrade)
