import pygame
from pygame.locals import *
from sys import exit
from random import randrange
from snake import *

pixelX = 900
pixelY = 600
length = 15







pygame.init()

screen = pygame.display.set_mode((pixelX, pixelY), 0, 32)

pygame.display.set_caption("Greedy Snake Ver-1.0")

# index: 0 for x-axis, 1 for y-axis
direct = [1, 0]

body = snake()
food = foodClass()


inputCount = 0
while True:
    inputCount = 0
    pygame.time.delay(50)
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()

        if event.type == KEYDOWN:
            if inputCount == 1:
                continue
            if event.key == K_LEFT:
                if direct[0] == 0:
                    direct[0] = -1
                    direct[1] = 0
                    inputCount += 1
            elif event.key == K_RIGHT:
                if direct[0] == 0:
                    direct[0] = 1
                    direct[1] = 0
                    inputCount += 1
            elif event.key == K_UP:
                if direct[1] == 0:
                    direct[1] = -1
                    direct[0] = 0
                    inputCount += 1
            elif event.key == K_DOWN:
                if direct[1] == 0:
                    direct[1] = 1
                    direct[0] = 0
                    inputCount += 1

    # if len(body) == 1:
    #     body[0].left += direct[0] * length
    #     body[0].top += direct[1] * length

    #     body[0].left %= pixelX
    #     body[0].top %= pixelY

    #     if (body[0].colliderect(food.collideBox)):
    #         body.append(Rect(body[0].left - direct[0]*length, body[0].top - direct[1]*length, length, length))
    #         randomFood(food.collideBox)
    # else:
        # if food.collidepoint(body[0].left + direct[0] * length, body[0].top + direct[1] * length):
        #     newHead = Rect(food.collideBox.left, food.collideBox.top, length, length)
        #     body.insert(0, newHead)
        #     randomFood(food.collideBox)
        # else:
        #     body[-1].left = body[0].left + direct[0] * length
        #     body[-1].top = body[0].top + direct[1] * length

        #     body[-1].left %= pixelX
        #     body[-1].top %= pixelY


        #     body.insert(0, body[-1])
        #     body.pop(-1)
        #     if isDead(body):
        #         pygame.time.delay(1000)
        #         print("you lose")
        #         exit()
    
    body.move(direct)

    if body.isDead():
        pygame.time.delay(1000)
        print("you lose")
        exit()


    if body.collide(food):
        body.append()
        
            
    screen.fill((0, 0, 0))

    body.show(screen)

    food.show(screen)

    pygame.display.update()