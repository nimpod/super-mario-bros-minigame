import pygame
import os
import Utils


class Player(pygame.sprite.Sprite):

    def __init__(self, x, y):
        self.width = 23
        self.height = 34
        self.velocity = 3
        self.dx = self.velocity
        self.dy = self.velocity
        self.username = ""

        self.imagenum = 1
        self.oldTime = 0

        pygame.sprite.Sprite.__init__(self)
        self.setImage(Utils.bombImages[self.imagenum])
        self.rect = self.image.get_rect()

        self.radius = (self.width+self.height)//6
        # pygame.draw.circle(self.image, (0,0,0), self.rect.center, self.radius)    # Draw the players hitbox
        
        self.rect.center = (x,y)


    def animate(self, updateEvery, totalTime):
        if (totalTime - self.oldTime >= updateEvery):
            if (self.imagenum == 0):
                self.imagenum = 1
            elif (self.imagenum == 1):
                self.imagenum = 0
            self.setImage(Utils.bombImages[self.imagenum])
            self.oldTime = totalTime


    def setImage(self, newImg):
        self.image = pygame.transform.scale(newImg, (self.width, self.height))
        self.image.set_colorkey((255,255,255))

    def setUsername(self, username):
        self.username = username

    def moveUp(self):
        self.rect.y -= self.dy

    def moveDown(self):
        self.rect.y += self.dy
    
    def moveLeft(self):
        self.rect.x -= self.dx

    def moveRight(self):
        self.rect.x += self.dx

    @property
    def getX(self):
        return self.rect.x

    @property
    def getY(self):
        return self.rect.y

    @property
    def getWidth(self):
        return self.width

    @property
    def getHeight(self):
        return self.height