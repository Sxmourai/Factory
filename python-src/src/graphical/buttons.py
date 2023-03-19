from pygame_gui.elements import UIButton
import pygame

class ConfigButton(UIButton):
    def __init__(self, relative_rect:pygame.Rect|tuple[float, float]|pygame.Vector2, text: str, manager=None, container=None, tool_tip_text:str=None, object_id:str=None, anchors: dict[str, str]=None, visible: int = 1):
        super().__init__(relative_rect, text, manager, container, tool_tip_text, object_id=object_id, anchors=anchors, visible=visible)
        self.buttons = [self, UIButton(relative_rect, "", manager, container, tool_tip_text, object_id="@INPUT", anchors=anchors)]