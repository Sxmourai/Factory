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
            self.panel.hide()
        else: self.panel.show()

    def button(self, img_path:str, text:str, description:str="", func=None, *args) -> int:
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
        button_container.description = UITextBox(f"<font size=2.5>{description}</font>", descr_rect, self.manager, container=button_container.container)

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
                    building.DESCRIPTION, self.game.event_controller.construct_overlay, building)
    def toggle(self):
        if len(self.buttons) == 0:
            buildings = [Factory, Core, Generator]
            for building in buildings:
                self.add_building(building)
        super().toggle()

# class Gui(Sprite):
#     def __init__(self, imgpath, font, title, size=None) -> None:
#         if size == None:
#             size_factor = .6
#             size = (surf_width()*size_factor,surf_height()*size_factor)
#         super().__init__(sc_center(), size, imgpath)
#         self.font = font
#         self._text = title
#         self.text = font.render(title, True, (0, 0, 0))
#         self.buttons = {}
#     def actualise_text(self, new_text:Optional[str]=None, new_font=None):
#         if new_text and new_font: self.text = new_font.render(new_text, True, (0, 0, 0))
#         elif new_text: self.text = self.font.render(new_text, True, (0, 0, 0))
#         elif new_font: self.text = new_font.render(self._text, True, (0, 0, 0))
#     def draw(self):
#         center = ((surf_width()-self.w)/2, (surf_height()-self.h)/2)
#         self.camera.render(self.img, center, self.size)
#         self.camera.render_text(self.text, ((surf_width()/2), 180))
#         for button in self.buttons.values():
#             button.draw()
#     def add_button(self, id, text, size, *args, **kwargs):
#         x = surf_width()/2-size[0]/2
#         y = 50*len(self.buttons)+surf_height()/2-50
#         self.button(id, Button("button.png", text, (x,y), size, *args, **kwargs))
#     def button(self, id:str, button):
#         self.buttons[id] = button
#     def handleClick(self, mpos):
#         if self.camera.collide(self.pos, self.size, mpos):
#             for button in self.buttons.values():
#                 button.handleClick(mpos)
#             return True
#         return False
#     def handleHover(self, mpos):
#         to_return = True
#         for button in self.buttons.values():
#             if button.handleHover(mpos): to_return = False
#         return to_return

# class FactoryGui(Gui):
#     def __init__(self, factory) -> None:
#         super().__init__("gui.png", sysFont(30), f"Tier {factory.gen}")
#         self.add_button("retrieve", "Retrieve", (150,40), onClick=factory.retrieve)
#         self.add_button("upgrade", f"Upgrade ({factory.COST})", (150,40), onClick=factory.upgrade)
#         self.factory = factory

# class CoreGui(Gui):
#     def __init__(self, core) -> None:
#         super().__init__("gui.png", sysFont(30), f"Tier {core.tier}")
#         #self.add_button(0, "Retrieve", (150,40), onClick=self.retrieve)
#         self.core = core


# class Button(Sprite):
#     def __init__(self, imgpath, text, pos, size, onClick=None,onHover=None) -> None:
#         super().__init__(pos, size, imgpath)
#         self.background = (0,0,0)
#         self.onClick = onClick
#         self.onHover = onHover
#         self._text = text
#         self.text = sysFont(30).render(text, True, (255,255,255))
        
#     def actualise_text(self, new_text:Optional[str]=None, new_font=None, color:tuple=(255,255,255)):
#         if new_text and new_font: self.text = new_font.render(new_text, True, color)
#         elif new_text: self.text = sysFont(30).render(new_text, True, color)
#         elif new_font: self.text = new_font.render(self._text, True, color)
        
#     def handleClick(self, mpos):
#         if self.rect.collidepoint(*mpos):
#             if type(self.onClick) is tuple:
#                 self.onClick[0](*self.onClick[1])
#             elif callable(self.onClick):
#                 self.onClick()
#             return True
#         return False

#     def handleHover(self, mpos):
#         collide = self.rect.collidepoint(*mpos)
#         if self.onHover and collide:
#             if type(self.onHover) is tuple:
#                 self.onHover[0](*self.onHover[1])
#             elif callable(self.onHover):
#                 self.onHover()
#         return collide
#     def draw(self):
#         pygame.draw.rect(self.surf, self.background, self.rect)
#         self.camera.render_text(self.text, (self.x+self.w/2,self.y+self.h/2))


# class GuiButton(Button):
#     W = 150
#     H = 40
#     def __init__(self, text, gui, onClick=None) -> None:
#         pos = len(gui.buttons)*self.H, sc_center(gui.surf)[0]
#         super().__init__(text, pos, (self.W,self.H), onClick, self._onHover)
#     def _onHover(self):
#         self.background = (255,255,255)