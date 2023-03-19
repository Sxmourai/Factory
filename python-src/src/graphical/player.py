import pygame
from src.ressources import Sprite, TW, TH

class Player(Sprite):
    SPEED = .1
    def __init__(self, pos: tuple | None, pseudo:str) -> None:
        super().__init__(pos, (40,40), "player")
        self.pseudo = pseudo
        self.next_pos = pos

    def draw(self):
        if self.next_pos[0] > self.x+Player.SPEED/2:
            self.x += Player.SPEED
        elif self.next_pos[0] < self.x-Player.SPEED/2:
            self.x -= Player.SPEED
        if self.next_pos[1] > self.y+Player.SPEED/2:
            self.y += Player.SPEED
        elif self.next_pos[1] < self.y-Player.SPEED/2:
            self.y -= Player.SPEED
        
        
        self.app.game.camera.draw_on_tile(self.img, self.pos, (40,40), transform=True)
        
        self.app.game.camera.render_text(self.pseudo, 10, (self.x*TW, self.y*TH-50), color=(255,255,255))
        