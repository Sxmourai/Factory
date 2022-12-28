import pygame
import pygame_gui
from random import choice
stri = "abcdefghijklmnopqrstuvwxyz"
pygame.init()

pygame.display.set_caption('Quick Start')
window_surface = pygame.display.set_mode((800, 600))

background = pygame.Surface((800, 600))
background.fill(pygame.Color('#ffffff'))

manager = pygame_gui.UIManager((800, 600), 'C:\\Users\\Sxmourai\\Documents\\Projets\\Python - Factory\\testing\\theme.json')

hello_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 275), (100, 50)),
                                            text='Retrieve',
                                            manager=manager)
text = pygame_gui.elements.UITextBox("<font color=gradient_text size=4.5><u>hello people</font>",pygame.Rect(0,0,400,80),manager)

clock = pygame.time.Clock()
is_running = True

while is_running:
    time_delta = clock.tick(60)/1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        if event.type == pygame_gui.UI_BUTTON_START_PRESS:
            if event.ui_element == hello_button:
                print('Hello World!')

        manager.process_events(event)

    manager.update(time_delta)

    window_surface.blit(background, (0, 0))
    manager.draw_ui(window_surface)

    pygame.display.update()