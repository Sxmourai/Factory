"""Module providing game core."""
import pygame
from game import Game
from ressources import rprint
pygame.init()

game = Game((100,100), (600,500))
core = game.core((4, 4))
fac = game.factory((0, 1), 1)
fac2 = game.factory((0, 0), 2)

clock = pygame.time.Clock()
running = True
while running:
    # fac.output()
    # fac2.output()
    game.draw()
    game.handleKeys(pygame.key.get_pressed())
    running = game.handleEvents(pygame.event.get())
    game.map.tile_in_screen(pygame.mouse.get_pos())

    clock.tick(60)

pygame.quit()