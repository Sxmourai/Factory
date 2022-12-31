from src.graphical.graphical import ButtonImage
from src.ressources import get_manager, sc_center, surf_width, surf_height, get_game
import pygame_gui
from pygame_gui.elements import UIPanel, UIButton, UILabel, UITextBox, UIWindow, UIImage
from pygame_gui.ui_manager import UIContainer
import pygame

from src.world.buildings import Core, Factory, Generator

class Menu:
    def __init__(self) -> None:
        rect = pygame.Rect(0,0, surf_width()*.7, surf_height()*.7)
        rect.center = sc_center()
        self.manager = get_manager()
        self.panel = UIPanel(rect, 1, self.manager) # UI(rect, self.manager)

        self.buttons = []
        self.panel.hide()

    def toggle(self):
        if self.panel.visible:
            self.hide()
        else: self.show()

    def hide(self): self.panel.hide()
    def show(self): self.panel.show()

    def button(self, img_path:str|UIImage, text:str, description:str="", func=None, *args) -> int:
        p_width = self.panel.get_relative_rect().w
        w,h = p_width*.8,70

        rect = pygame.Rect(0,30+len(self.buttons)*h,w,h)
        rect.centerx = p_width/2
        button_container = ButtonImage(rect, img_path, "", self.panel, ((5,5),(h-10,h-10)))

        label_rect = pygame.Rect(0,5, 100, 20)
        label_rect.centerx = w/2+15

        button_container.title = UILabel(label_rect, text, self.manager, container=button_container.container)
        descr_rect = pygame.Rect(0, 20, w*.8, h-20)
        descr_rect.centerx = w/2+15
        button_container.description = UITextBox(f"<font size=2.5>{description}</font>", descr_rect, self.manager, container=button_container.container, object_id="#construct_desc")

        self.buttons.append((button_container, func, args))
        return button_container
    def handle_event(self, event):
        for button,func,args in self.buttons:
            if event.ui_element == button.button:
                func(*args)

class ConstructMenu(Menu):
    def __init__(self) -> None:
        super().__init__()
        self.game = get_game()
        UILabel(pygame.Rect(5,5,-1,-1), "Construction menu",self.manager, self.panel)

    def add_building(self, building):
        self.button(building.IMG_PATH, building.TITLE,
                    building.DESCRIPTION, self.game.event_controller.enter_construction_mode, building)
    def toggle(self):
        if len(self.buttons) == 0:
            buildings = [Factory, Core, Generator]
            for building in buildings:
                self.add_building(building)
        super().toggle()
