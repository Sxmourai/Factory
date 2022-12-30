from pygame_gui.elements import UIButton, UIImage
from pygame_gui.ui_manager import UIContainer
import pygame

from src.ressources import load, get_manager

class ButtonImage:
    def __init__(self, rect:pygame.Rect, img_path:str|UIImage, text:str="", container=None,
                       img_pos_n_size:tuple[tuple[int,int],tuple[int,int]]=None, button_rect:pygame.Rect=None) -> None:
        self.rect = rect
        self.manager = get_manager()
        self.container = UIContainer(rect, self.manager, container=container)
        b_rect = button_rect if button_rect else pygame.Rect(0,0,*rect.size)
        self.button = UIButton(b_rect, text, self.manager, self.container)
        if isinstance(img_path, UIImage):
            self.image = img_path
        else:
            self.img = load(img_path, rect.size)
            rect = pygame.Rect(*img_pos_n_size[0], *img_pos_n_size[1]) if img_pos_n_size else pygame.Rect(0,0, rect.h-2, rect.h-2)
            self.image = UIImage(rect, self.img, self.manager, container=self.container)
