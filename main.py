import pygame
from pygame.locals import *
from sys import exit
from random import randrange

def randomFood(food):
    food.left = randrange(0, 600, 10)
    food.top = randrange(0, 400, 10)

def isDead(body):
    head = body[0]
    for i in range(1, len(body)):
        if head.colliderect(body[i]):
            return True

    return False

pygame.init()

screen = pygame.display.set_mode((600, 400), 0, 32)

pygame.display.set_caption("Greedy Snake Ver-1.0")

# index: 0 for x-axis, 1 for y-axis
direct = [1, 0]

body = [Rect(300, 200, 10, 10)]
food = Rect(200, 100, 10, 10)

while True:
    pygame.time.delay(100)
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()

        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                if direct[0] ==0:
                    direct[0] = -1
                    direct[1] = 0
            elif event.key == K_RIGHT:
                if direct[0] ==0:
                    direct[0] = 1
                    direct[1] = 0
            elif event.key == K_UP:
                if direct[1] ==0:
                    direct[1] = -1
                    direct[0] = 0
            elif event.key == K_DOWN:
                if direct[1] ==0:
                    direct[1] = 1
                    direct[0] = 0
        # elif event.type == KEYUP:
        #     if event.key == K_LEFT or event.key == K_RIGHT:
        #         direct[0] = 0
        #     elif event.key == K_UP or event.key == K_DOWN:
        #         direct[1] = 0

    if len(body) == 1:
        body[0].centerx += direct[0] * 10
        body[0].centery += direct[1] * 10
        # TODO too ugly
        if body[0].centerx >= 600:
            body[0].centerx -= 600
        elif body[0].centerx < 0:
            body[0].centerx += 600
        if body[0].centery >= 400:
            body[0].centery -= 400
        elif body[0].centery < 0:
            body[0].centery += 400

        if (body[0].colliderect(food)):
            body.append(Rect(body[0].left - direct[0]*10, body[0].top - direct[1]*10, 10, 10))
            randomFood(food)
    else:
        if food.collidepoint(body[0].centerx + direct[0] * 10, body[0].centery + direct[1] * 10):
            newHead = Rect(food.left, food.top, 10, 10)
            body.insert(0, newHead)
            randomFood(food)
        else:
            body[-1].left = body[0].left + direct[0] * 10
            body[-1].top = body[0].top + direct[1] * 10

            # TODO: Too ugly
            if body[-1].left >= 600:
                body[-1].left -= 600
            elif body[-1].left < 0:
                body[-1].left += 600
            if body[-1].top >= 400:
                body[-1].top -= 400
            elif body[-1].top < 0:
                body[-1].top += 400


            body.insert(0, body[-1])
            body.pop(-1)
            if isDead(body):
                pygame.time.delay(1000)
                print("you lose")
                exit()
            
    
    screen.fill((0, 0, 0))
    for aRect in body:
        pygame.draw.rect(screen, Color(0, 255, 0, 255), aRect, 0)
    pygame.draw.rect(screen, Color(255,255,255,255), food)

    pygame.display.update()