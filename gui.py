from ressources import load, sysFont, Shape, sc_center
import pygame


class Gui(Shape):
    def __init__(self, imgpath, font, title, size, game) -> None:
        self.surf = game.surf
        super().__init__(*sc_center(self.surf), *size)
        self.camera = game.camera
        self.map = game.map
        self.game = game
        self.img = load(imgpath, size)
        self.text = font.render(title, True, (0, 0, 0))
        self.buttons = []
        
    def draw(self):
        center = ((self.surf.get_width()-self.w)/2, (self.surf.get_height()-self.h)/2)
        self.camera.render(self.img, center, self.size)
        self.camera.render_text(self.text, ((self.surf.get_width()/2), 180))
        for button in self.buttons:
            button.draw()
    def add_button(self, order, text, size, *args, **kwargs):
        x = self.surf.get_width()/2-size[0]/2
        y = 210+(50*order)
        pos = x,y
        self.buttons.append(Button("button.png", text, pos, size, self.map, *args, **kwargs))
    def handleClick(self, mpos):
        for button in self.buttons:
            button.handleClick(mpos)
    def handleHover(self, mpos):
        for button in self.buttons:
            button.handleHover(mpos)

class FactoryGui(Gui):
    def __init__(self, factory) -> None:
        super().__init__("gui.png", sysFont(30), f"Tier {factory.gen}", (200,200), factory.game)
        self.add_button(0, "Retrieve", (150,40), onClick=self.retrieve)
        self.factory = factory
    def retrieve(self):
        self.factory.retrieve()

class Button:
    def __init__(self, imgpath, text, pos, size, game, onClick=None,onHover=None) -> None:
        self.size = size
        self.x, self.y = pos
        self.size = size
        self.img = load(imgpath, self.size)
        self.rect = pygame.Rect(self.x, self.y, *self.size)
        self.background = (0,0,0)
        self.onClick = onClick
        self.onHover = onHover
        self.map = game.map
        self.game = game
        self.surf = game.surf
        self.camera = game.camera
        self.text = sysFont(30).render(text, True, (255,255,255))
    def handleClick(self, mpos):
        if self.rect.collidepoint(*mpos):
            if type(self.onClick) is tuple:
                self.onClick[0](*self.onClick[1])
            elif callable(self.onClick):
                self.onClick()

    def handleHover(self, mpos):
        collide = self.rect.collidepoint(*mpos)
        if self.onHover:
            if type(self.onHover) is tuple:
                self.onHover[0](*self.onHover[1])
            elif callable(self.onHover):
                self.onHover()
        if collide: self.background = (255,255,255)
        else: self.background = (0,0,0)
        return collide
    def draw(self):
        self.rect = pygame.Rect(self.x, self.y, *self.size)
        pygame.draw.rect(self.surf, self.background, self.rect)
        self.camera.render_text(self.text, (self.x+self.size[0]/2,self.y+self.size[1]/2))

