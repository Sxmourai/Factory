from camera import Camera
from world import Map
from ressources import load, transform, sysFont
from gui import Button
from buildings import Factory, Core
import pygame
from time import time

class Game:
    PLAYER_SIZE = (30,30)
    PLAYER_IMAGE = load("player.png", PLAYER_SIZE)
    def __init__(self, size, screen_size):
        self.surf = pygame.display.set_mode(screen_size)
        self.camera = Camera((0,0), self.surf)
        self.map = Map(size, self)
        self.guis  = {}
        self.texts = {}
        self.buttons = []
        self._life = time()
        self._tick = 0
        self.points = self.setup_points()
    def get_life(self):
        return time()-self._life
    
    def tick(self, need_set_tick:bool=True):
        if need_set_tick:
            self._tick = (pygame.time.get_ticks() - self._tick) / 10
        return self._tick
    
    def draw(self):
        self.tick()
        self.map.draw()
        self.camera.render(self.PLAYER_IMAGE, self.screen_center(),transform(self.PLAYER_SIZE))
        for gui in self.guis.values():
            gui.draw()
        for button in self.buttons:
            button.draw()        
        for text, textRect in self.texts.values():
            self.camera.render_textRect(text, textRect)
    
        pygame.display.flip()
        
    def screen_center(self):
        return (self.surf.get_width()/2, self.surf.get_height()/2)

    def handleKeys(self, keys):
        if keys:
            if keys[pygame.K_UP]:
                self.camera.move(180, keys[pygame.K_SPACE])
            if keys[pygame.K_DOWN]:
                self.camera.move(0, keys[pygame.K_SPACE])
            if keys[pygame.K_RIGHT]:
                self.camera.move(90, keys[pygame.K_SPACE])
            if keys[pygame.K_LEFT]:
                self.camera.move(270, keys[pygame.K_SPACE])
                
    def handleEvents(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONUP:
                self.click(pygame.mouse.get_pos())
            elif event.type == pygame.MOUSEMOTION:
                self.hover(pygame.mouse.get_pos())
        return True
    
    def add_points(self, points):
        self.points += int(points)
        self.texts[0] = self.camera.render_text(self.points, 30, (40,15))
    def setup_points(self):
        self.texts[0] = self.camera.render_text("0", 30, (40,15))
        return 0
    
    def add_button(self, order, size):
        self.buttons.append(Button("button.png", order, size, self.map))
        
    def click(self, mpos):
        self.map.click(mpos)
        for gui in self.guis.values():
            gui.handleClick(mpos)
        for button in self.buttons:
            button.handleClick(mpos)
            
    def hover(self, mpos):
        self.map.hover(mpos)
        for button in self.buttons:
            button.handleHover(mpos)
            
    def factory(self,pos:tuple, tier:int):
        return Factory(pos, tier, self)
    def core(self,pos:tuple):
        return Core(pos, self)