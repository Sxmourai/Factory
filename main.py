"""Module providing game core."""
import pygame
from src.main.app import Application
pygame.init()
pygame.display.set_caption('Factory game')
app = Application((1000,800))
RUNNING = True
while RUNNING:
    try:
        RUNNING = app.run()
    except KeyboardInterrupt:
        app.exit()


pygame.quit()