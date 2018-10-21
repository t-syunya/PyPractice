import pygame

BLACK = (0, 0, 0)
RED = (255, 0, 0)

pygame.init()
screen = pygame.display.set_mode((640, 480))
myclock = pygame.time.Clock()
screen.fill(BLACK)

rect = (200, 100, 100, 100)
pygame.draw.rect(screen, RED, rect)
pygame.display.flip()

flag = 0
while flag == 0:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: flag = 1
    myclock.tick(60)

pygame.quit()
