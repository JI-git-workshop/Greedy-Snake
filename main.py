import pygame
from pygame.locals import *
from sys import exit
from random import randrange
from snake import *

pixelX = 900
pixelY = 600
length = 15


def randomFood(aRect):
    aRect.left = randrange(0, pixelX, length)
    aRect.top = randrange(0, pixelY, length)
    return aRect

class foodClass:
    state = [-1, 0, 0, 1, 1, 1, 1, 0, 0, -1]
    def __init__(self):
        self.image = pygame.image.load("Strawberry-15x15.png")
        self.collideBox = randomFood(Rect(200, 100, length, length))
        self.time = 2
    
    def collidepoint(self, x, y):
        return self.collideBox.collidepoint(x, y)

    def show(self, screen):
        self.time += 1
        self.time %= 10
        screen.blit(self.image,(self.collideBox.left, self.collideBox.top + self.state[self.time]))


def isDead(body):
    head = body[0]
    for i in range(1, len(body)):
        if head.colliderect(body[i]):
            return True

    return False

pygame.init()

screen = pygame.display.set_mode((pixelX, pixelY), 0, 32)

pygame.display.set_caption("Greedy Snake Ver-1.0")

# index: 0 for x-axis, 1 for y-axis
direct = [1, 0]

body = [Rect(randrange(0, pixelX, length), randrange(0, pixelY, length), length, length)]
food = foodClass()


inputCount = 0
while True:
    inputCount = 0
    pygame.time.delay(100)
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

    if len(body) == 1:
        body[0].left += direct[0] * length
        body[0].top += direct[1] * length

        body[0].left %= pixelX
        body[0].top %= pixelY

        if (body[0].colliderect(food.collideBox)):
            body.append(Rect(body[0].left - direct[0]*length, body[0].top - direct[1]*length, length, length))
            randomFood(food.collideBox)
    else:
        if food.collidepoint(body[0].left + direct[0] * length, body[0].top + direct[1] * length):
            newHead = Rect(food.collideBox.left, food.collideBox.top, length, length)
            body.insert(0, newHead)
            randomFood(food.collideBox)
        else:
            body[-1].left = body[0].left + direct[0] * length
            body[-1].top = body[0].top + direct[1] * length

            body[-1].left %= pixelX
            body[-1].top %= pixelY


            body.insert(0, body[-1])
            body.pop(-1)
            if isDead(body):
                pygame.time.delay(1000)
                print("you lose")
                exit()
            
    screen.fill((0, 0, 0))
    for aRect in body:
        pygame.draw.rect(screen, Color(0, 255, 0, 255), aRect, 0)
    # pygame.draw.rect(screen, Color(255,255,255,255), food)
    food.show(screen)

    pygame.display.update()