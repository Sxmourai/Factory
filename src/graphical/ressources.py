
from pygame_gui.elements import UITextBox, UIButton, UIPanel, UILabel, UIScrollingContainer, UITextEntryLine, UIImage, UIWindow
from pygame_gui.core import ObjectID
from pygame_gui.ui_manager import UIContainer
from abc import ABC, abstractmethod
from src.ressources import *


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
