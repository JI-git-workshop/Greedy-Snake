import pygame
from pygame.locals import *
from sys import exit


pygame.init()

screen = pygame.display.set_mode((600, 400), 0, 32)

pygame.display.set_caption("hello world")

moveX = 0
moveY = 0
# speed = [0, 0]
# acceleration = 1
pos = [300, 200]
# aBlock = pygame.draw.rect(screen, Color(0, 255, 0, 255), (pos[0], pos[1], 10, 10), 0)

while True:
    pygame.time.delay(20)
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()

        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                moveX = -1
                # aBlock.move(-10, 0)
            elif event.key == K_RIGHT:
                moveX = 1
                # aBlock.move(10, 0)
            elif event.key == K_UP:
                moveY = -1
                # aBlock.move(0, 10)
            elif event.key == K_DOWN:
                moveY = 1
                # aBlock.move(0, -10)
        elif event.type == KEYUP:
            if event.key == K_LEFT or event.key == K_RIGHT:
                moveX = 0
            elif event.key == K_UP or event.key == K_DOWN:
                moveY = 0

   
    pos[0] += moveX * 2
    pos[1] += moveY * 2
    
    screen.fill((0, 0, 0))
    # aBlock.move(pos[0], pos[1])
    pygame.draw.rect(screen, Color(0, 255, 0, 255), (pos[0], pos[1], 10, 10), 0)

    pygame.display.update()