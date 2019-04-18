import pygame
import random
from Utils import *

class Enemy(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.width = 213
        self.height = 180

        self.image = bowser_img
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()
        self.rect.x = WINDOW_WIDTH//1.9        # initially put Bowser in centre of screen
        self.rect.y = WINDOW_HEIGHT//32
        self.velocity = 1.0
        self.dx = self.velocity

        self.newX = 0
        self.moving = False
        self.shooting = False

    def move(self):
        if (self.rect.x > 0 and self.rect.x < WINDOW_WIDTH -self.width//1.6):
            self.rect.x += self.dx

    #def update(self):
     #   if self.moving == True:
      #      self.rect.x += self.dx      # move to the new x-coord

    def generateNewX(self):
        min = 0
        max = WINDOW_WIDTH -self.width//1.6
        self.newX = random.randrange(min, max)

        # change the x-direction depending on the new x-coordinate
        multiplier = 1.0 if (self.rect.x < self.newX) else -1.0
        self.dx = self.velocity * multiplier
        
        return self.newX

    def direction(self):
        if self.dx < 0:
            return "Going left"
        else:
            return "Going right"

    # GETTERS
    def getRectX(self):
        return self.rect.x

    def getRectY(self):
        return self.rect.y

    def getNewX(self):
        return self.newX

    def getDx(self):
        return self.dx

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height

    def getMoving(self):
        return self.moving
    
    def getShooting(self):
        return self.shooting

    # SETTERS
    def setNewX(self, newX):
        self.newX = newX

    def setMoving(self, moving):
        self.moving = moving

    def setShooting(self, shooting):
        self.shooting = shooting


class Fire(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.radius = 30

        self.image_orig = bowserFire_img
        self.image_orig = pygame.transform.scale(self.image_orig, (self.radius, self.radius))
        self.image_orig.set_colorkey((255,255,255))
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.velocity = 3.0
        self.dy = self.velocity*1.0

        self.rotationAngle = 0
        self.rotationVelocity = random.randrange(-8,8)
        self.lastUpdate = pygame.time.get_ticks()
    
    def update(self):
        self.rect.y += self.dy
        self.rotate()
        
    def rotate(self):
        now = pygame.time.get_ticks()
        # every 30ms...
        if (now - self.lastUpdate >= 15):
            self.lastUpdate = now
            self.rotationAngle = (self.rotationAngle + self.rotationVelocity) % 360         # loop the angle back to 0 when it reaches 360
            self.image = pygame.transform.rotate(self.image_orig, self.rotationAngle)
            '''new_image = pygame.transform.rotate(self.image_orig, self.rotationVelocity)    # rotate the fire
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center'''
