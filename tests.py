import pygame
pygame.init()
screen = pygame.display.set_mode((500,500), 0, 0, 0, 0)
clock = pygame.time.Clock()
while True:
    screen.fill((255,255,255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
    clock.tick(60)
    pygame.draw.circle(screen, (255,0,0), (250,250), 40)
    pygame.draw.polygon(screen, (255,0,0), [(5,5), (10,10),(20,10), (25,5)])
    pygame.display.flip()