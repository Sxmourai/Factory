"""Module providing game core."""
import pygame
from game import Game
from menu import Menu
from ressources import rprint
pygame.init()
pygame.display.set_caption('Factory game')
game = Game((100,100), (1000,700), ticks=60)
running = True
while running:
    game.draw()
    game.handleKeys(pygame.key.get_pressed())
    running = game.handleEvents(pygame.event.get())

pygame.quit()