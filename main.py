"""Module providing game core."""
import pygame
from src.main.game import Game
pygame.init()
pygame.display.set_caption('Factory game')
game = Game((100,100), (1000,700), ticks=60)
RUNNING = True
while RUNNING:
    game.draw()
    game.handle_keys(pygame.key.get_pressed())
    RUNNING = game.handle_events(pygame.event.get())

pygame.quit()