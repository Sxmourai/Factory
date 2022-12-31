from typing import Dict, Iterable, Optional, Tuple, Union
from pygame_gui.elements import UIButton, UIImage
from pygame_gui.ui_manager import UIContainer
from pygame_gui.core import ObjectID,IContainerLikeInterface, UIElement
import pygame

from src.ressources import load, get_manager

class ButtonImage:
    def __init__(self, rect:pygame.Rect, img_path:str|UIImage|pygame.Surface, text:str="", container=None,
                       img_pos_n_size:tuple[tuple[int,int],tuple[int,int]]=None, button_rect:pygame.Rect=None) -> None:
        self.rect = rect
        self.manager = get_manager()
        self.container = UIContainer(rect, self.manager, container=container)
        b_rect = button_rect if button_rect else pygame.Rect(0,0,*rect.size)
        self.button = UIButton(b_rect, text, self.manager, self.container)
        if isinstance(img_path, UIImage):
            self.image = img_path
        else:
            if isinstance(img_path, pygame.Surface):
                self.img = img_path
            else: self.img = load(img_path, rect.size)
            rect = pygame.Rect(*img_pos_n_size[0], *img_pos_n_size[1]) if img_pos_n_size else pygame.Rect(0,0, rect.h-2, rect.h-2)
            self.image = UIImage(rect, self.img, self.manager, container=self.container)

class ButtonLogo:
    def __init__(self, img_path:str, relative_rect: pygame.Rect|Tuple[float, float]|pygame.Vector2, container:IContainerLikeInterface=None, tool_tip_text:str=None, object_id:ObjectID|str=None, anchors:Dict[str, Union[str, UIElement]] = None, allow_double_clicks: bool = False):
        self.manager = get_manager()
        self.container = UIContainer(relative_rect, self.manager, container=container)
        self.button = UIButton(relative_rect, "", self.manager, self.container, tool_tip_text, object_id=object_id, anchors=anchors, allow_double_clicks=allow_double_clicks)
        image_rect = relative_rect.copy()
        image_rect.w = relative_rect.w * .7
        image_rect.h = relative_rect.h * .7
        image_rect.center = relative_rect.w/2, relative_rect.h/2
        self.imageLogo = UIImage(image_rect, load(img_path), self.manager, container=self.container)