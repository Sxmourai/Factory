import pygame
from src.ressources import Sprite
class Player(Sprite):
    def __init__(self, pos: tuple | None, pseudo:str) -> None:
        super().__init__(pos, (40,40), "player")
        self.pseudo = pseudo