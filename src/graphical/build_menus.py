import pygame
from pygame_gui.elements import UIPanel, UIButton, UILabel
from src.ressources import *
from src.graphical.ressources import SimpleMenu


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

class FactoryMenu(BuildingMenu):
    def __init__(self, factory) -> None:
        super().__init__(factory, "Factory menu")
        self.points = UILabel(pygame.Rect(0,-100,100,50),"")
        self.retrieve = self.button("Retrieve", "Click to retrieve points", factory.retrieve)
        self.upgrade = self.button("Upgrade", "Click to upgrade this factory", factory.upgrade)
