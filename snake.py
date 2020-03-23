import pygame
from pygame.locals import *
from sys import exit
from random import randrange


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
        if self.collideBox.collidepoint(x, y):
            randomFood(self.collideBox)
            return True
        return False

    def show(self, screen):
        self.time += 1
        self.time %= 10
        screen.blit(self.image,(self.collideBox.left, self.collideBox.top + self.state[self.time]))


class bodyGeneral:
    def __init__(self, component = None, direction = [1, 0]):
        self.component = component
        self.image = None
        if component != None:
            self.image = pygame.image.load(component + ".png")
        
        self.collideBox = Rect(0, 0, 15, 15)
        self.direction = direction

    def move(self, direction):
        originalDirection = self.direction[:]

        self.direction = direction[:]
        self.collideBox.left += direction[0] * 15
        self.collideBox.top += direction[1] * 15

        self.collideBox.left %= pixelX
        self.collideBox.top %= pixelY

        return originalDirection

        
    
    def show(self, screen):
        temp = self.image
        if self.component == "head":
            # store the angle of rotation
            rotation = [180, 90, 0, -90, 0]
            temp = pygame.transform.rotate(self.image, rotation[self.direction[0] * 2 + self.direction[1] + 2])
        elif self.component == "tail":
            rotation = [0, -90, 0, 90, 180]
            temp = pygame.transform.rotate(self.image, rotation[self.direction[0] * 2 + self.direction[1] + 2])
        elif self.component == "body":
            rotation = [180, 90, 0, -90, 0]
            temp = pygame.transform.rotate(self.image, rotation[self.direction[0] * 2 + self.direction[1] + 2])

            temp = pygame.transform.rotate(temp, 180 * self.state)
            self.state = 1 - self.state

        screen.blit(temp,(self.collideBox.left, self.collideBox.top))

# Only for the tail
    def turn(self, screen, preDirect):
        temp = self.image
        if self.component == "tail":
            rotation = [0, -90, 0, 90, 180]
            temp = pygame.transform.rotate(self.image, rotation[preDirect[0] * 2 + preDirect[1] + 2])

        pygame.draw.rect(screen,[0,0,0],self.collideBox,0)
        screen.blit(temp,(self.collideBox.left, self.collideBox.top))

class bodyS(bodyGeneral):
    def __init__(self, direction = [1,0]):
        bodyGeneral.__init__(self, "body", direction)
        # 0: up  1: down
        self.state = 0

    def turn(self, screen, preDirect):
        temp = pygame.image.load("connection.png")

        if preDirect[0] == 1 and preDirect[1] == 0 and self.direction[0] == 0 and self.direction[1] == -1:
            temp = pygame.transform.rotate(temp, 180)
        elif preDirect[0] == 0 and preDirect[1] == 1 and self.direction[0] == -1 and self.direction[1] == 0:
            temp = pygame.transform.rotate(temp, 180)
        if preDirect[0] == -1 and preDirect[1] == 0 and self.direction[0] == 0 and self.direction[1] == -1:
            temp = pygame.transform.rotate(temp, 90)
        elif preDirect[0] == 0 and preDirect[1] == 1 and self.direction[0] == 1 and self.direction[1] == 0:
            temp = pygame.transform.rotate(temp, 90)
        if preDirect[0] == -1 and preDirect[1] == 0 and self.direction[0] == 0 and self.direction[1] == 1:
            temp = pygame.transform.rotate(temp, 0)
        elif preDirect[0] == 0 and preDirect[1] == -1 and self.direction[0] == 1 and self.direction[1] == 0:
            temp = pygame.transform.rotate(temp, 0)
        if preDirect[0] == 1 and preDirect[1] == 0 and self.direction[0] == 0 and self.direction[1] == 1:
            temp = pygame.transform.rotate(temp, -90)
        elif preDirect[0] == 0 and preDirect[1] == -1 and self.direction[0] == -1 and self.direction[1] == 0:
            temp = pygame.transform.rotate(temp, -90)

        pygame.draw.rect(screen,[0,0,0],self.collideBox,0)
        screen.blit(temp,(self.collideBox.left, self.collideBox.top))

class snake:
    def __init__(self):
        self.body = [bodyGeneral("head", [1, 0]), bodyGeneral("tail", [1, 0])]
        self.body[0].collideBox.left = 300
        self.body[0].collideBox.top = 300
        self.body[1].collideBox.left = 285
        self.body[1].collideBox.top = 300
    
    def move(self, direction):
        for i in self.body:
            direction = i.move(direction)[:]
            # TODO When turning the direction is special
            # self.body[1].move(direction1)

    def show(self, screen):
        for i in self.body:
            i.show(screen)

        preDirect = self.body[0].direction[:]
        for i in range(1, len(self.body)):
            if preDirect[0] != self.body[i].direction[0] or preDirect[1] != self.body[i].direction[1]:
                self.body[i].turn(screen, preDirect)
                preDirect = self.body[i].direction[:]

    def append(self):
        tail = self.body[-1]
        newBody = bodyS(tail.direction[:])
        newBody.collideBox.left = tail.collideBox.left
        newBody.collideBox.top = tail.collideBox.top

        if len(self.body) >= 3:
            newBody.state = 1 - self.body[-2].state
        self.body.insert(-1, newBody)
        tail.collideBox.left -= tail.direction[0] * 15
        tail.collideBox.top -= tail.direction[1] * 15

    def collide(self, food):
        for i in self.body:
            if food.collidepoint(i.collideBox.left, i.collideBox.top):
                return True
        return False

    def isDead(self):
        head = self.body[0]
        for i in range(1, len(self.body)):
            if head.collideBox.colliderect(self.body[i].collideBox):
                return True
        return False




# if __name__ == "__main__":


#     pygame.init()
#     pygame.display.set_icon(pygame.image.load("Title-Image.png"))

#     screen = pygame.display.set_mode((pixelX, pixelY), 0, 32)

#     pygame.display.set_caption("Greedy Snake Ver-1.0")

#     # index: 0 for x-axis, 1 for y-axis
#     direct = [1, 0]

#     body = snake()


#     inputCount = 0
#     while True:
#         inputCount = 0
#         pygame.time.delay(250)
#         for event in pygame.event.get():
#             if event.type == QUIT:
#                 exit()

#             if event.type == KEYDOWN:
#                 if inputCount == 1:
#                     continue
#                 if event.key == K_LEFT:
#                     if direct[0] == 0:
#                         direct[0] = -1
#                         direct[1] = 0
#                         inputCount += 1
#                 elif event.key == K_RIGHT:
#                     if direct[0] == 0:
#                         direct[0] = 1
#                         direct[1] = 0
#                         inputCount += 1
#                 elif event.key == K_UP:
#                     if direct[1] == 0:
#                         direct[1] = -1
#                         direct[0] = 0
#                         inputCount += 1
#                 elif event.key == K_DOWN:
#                     if direct[1] == 0:
#                         direct[1] = 1
#                         direct[0] = 0
#                         inputCount += 1
#                 # elif event.key == K_m:
#                 #     body.append()

#         # if len(body) == 1:
#         #     body[0].left += direct[0] * length
#         #     body[0].top += direct[1] * length

#         #     body[0].left %= pixelX
#         #     body[0].top %= pixelY

#         # else:
#             # body[-1].left = body[0].left + direct[0] * length
#             # body[-1].top = body[0].top + direct[1] * length

#             # body[-1].left %= pixelX
#             # body[-1].top %= pixelY


#             # body.insert(0, body[-1])
#             # body.pop(-1)
#         body.move(direct)
                
#         screen.fill((0, 0, 0))


#         body.show(screen)
#         # for aRect in body:
#         #     pygame.draw.rect(screen, Color(0, 255, 0, 255), aRect, 0)

#         pygame.display.update()

