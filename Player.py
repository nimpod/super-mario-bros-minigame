import pygame
from os import path
import Utils


class Player(pygame.sprite.Sprite):

    def __init__(self, x, y, username):
        self.width = 23
        self.height = 34
        self.velocity = 3.0
        self.dx = self.velocity
        self.dy = self.velocity
        self.username = username
        self.score = 0
        self.dead = False

        self.imagenum = 1
        self.oldTime = 0

        pygame.sprite.Sprite.__init__(self)
        self.setImage(Utils.bombImages[self.imagenum])
        self.rect = self.image.get_rect()
        self.radius = (self.width+self.height)//10
        # pygame.draw.circle(self.image, (0,0,0), self.rect.center, self.radius)    # Draw the players hitbox
        self.rect.center = (x,y)

    def animate(self, updateEvery, totalTime):
        if (totalTime - self.oldTime >= updateEvery and self.dead == False):
            if (self.imagenum == 0):
                self.imagenum = 1
            elif (self.imagenum == 1):
                self.imagenum = 0            
            self.setImage(Utils.bombImages[self.imagenum])
            self.oldTime = totalTime

            # also make the bip-bob player sound whenever the animation changes            
            if Utils.playermoving == True:
                Utils.playerSound.play()

        elif (self.dead == True):
            self.setImage(Utils.bombdead)


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

    def setDead(self, dead):
        self.dead = dead

    def setScore(self, updatedScore):
        self.score = updatedScore