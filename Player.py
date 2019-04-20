import pygame
from os import path
from Utils import *


class Player(pygame.sprite.Sprite):

    def __init__(self, x, y, username):
        self.width = 23
        self.height = 34
        self.velocity = 3.0
        self.dx = self.velocity
        self.dy = self.velocity
        self.username = username
        self.score = 0
        self.moving = False

        self.imagenum = 1
        self.oldTime = 0

        pygame.sprite.Sprite.__init__(self)
        self.setImage(bombImages[self.imagenum])
        self.rect = self.image.get_rect()
        self.radius = (self.width+self.height)//10
        # pygame.draw.circle(self.image, (0,0,0), self.rect.center, self.radius)    # Draw the players hitbox
        self.rect.center = (x,y)

    def animate(self, updateEvery, totalTime):
        if (totalTime - self.oldTime >= updateEvery):
            if (self.imagenum == 0):
                self.imagenum = 1
            elif (self.imagenum == 1):
                self.imagenum = 0            
            self.setImage(bombImages[self.imagenum])
            self.oldTime = totalTime

            # also make the bip-bob player sound whenever the animation changes            
            if self.moving == True:
                playerSound.play()

    # SETTERS
    def setImage(self, newImg):
        self.image = pygame.transform.scale(newImg, (self.width, self.height))
        self.image.set_colorkey((255,255,255))

    def setUsername(self, username):
        self.username = username

    def setMoving(self, moving):
        self.moving = moving

    def setScore(self, updatedScore):
        self.score = updatedScore

    def setX(self, newX):
        self.rect.x = newX

    def setY(self, newY):
        self.rect.y = newY

    # MOVE PLAYER
    def moveUp(self):
        self.rect.y -= self.dy

    def moveDown(self):
        self.rect.y += self.dy
    
    def moveLeft(self):
        self.rect.x -= self.dx

    def moveRight(self):
        self.rect.x += self.dx

    # GETTERS
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

    @property
    def getRadius(self):
        return self.radius

    def getMoving(self):
        return self.moving

    def getCenter(self):
        return self.rect.center
    
    def getScore(self):
        return self.score

    def getUsername(self):
        return self.username



class Explosion(pygame.sprite.Sprite):
    
    def __init__(self, center, radius):
        pygame.sprite.Sprite.__init__(self)
        self.radius = radius
        self.image = explosionImages[0]
        self.image = pygame.transform.scale(self.image, (self.radius, self.radius))
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.lastUpdate = pygame.time.get_ticks()
        self.frameRate = 75

    def update(self):
        now = pygame.time.get_ticks()
        if (now - self.lastUpdate > self.frameRate):
            self.lastUpdate = now
            self.frame += 1
            if (self.frame == len(explosionImages)):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosionImages[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center