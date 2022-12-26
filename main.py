"""Module providing game core."""
import pygame
from game import Game
from ressources import rprint
pygame.init()

game = Game((100,100), (1000,700), ticks=60)
core = game.core((4, 4))
fac = game.factory((0, 1), 1)
fac2 = game.factory((0, 0), 2)

running = True
while running:
    # fac.output()
    # fac2.output()
    game.draw()
    game.handleKeys(pygame.key.get_pressed())
    running = game.handleEvents(pygame.event.get())

pygame.quit()