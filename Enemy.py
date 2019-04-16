import pygame
import random
import Utils

class Enemy(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.width = 213
        self.height = 180

        self.image = Utils.bowser
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()
        self.rect.x = Utils.windowWidth//1.85
        self.rect.center = (self.generateNewX(), Utils.windowHeight//6)

        self.velocity = 1.0
        self.dx = self.velocity
        self.dy = self.velocity
        self.newX = self.generateNewX()

        self.shooting = False
        self.moving = False

        self.timeStoppedMoving = 0
        self.lastShot = pygame.time.get_ticks()
        self.shotDelay = 400
        self.timeShooting = 5000
        self.timeStartedShooting = pygame.time.get_ticks()
        self.fires = pygame.sprite.Group()

    def update(self):
        # move bowser if he's not moving or shooting
        if (self.shooting == False and self.moving == False):
            self.moving = True
            self.setNewX()

        # keep moving bowser...
        if (self.moving == True):
            self.move()
            self.timeStoppedMoving = pygame.time.get_ticks()
            
            # until he reaches the new x-coord
            if (self.rect.x == self.newX):
                self.moving = False
                self.shooting = True
                self.timeStartedShooting = pygame.time.get_ticks()
        
        # shoot
        now = pygame.time.get_ticks()
        if (self.shooting == True and now - self.timeStoppedMoving >= 3000):
            self.shoot()
            if (now - self.timeStartedShooting >= self.timeShooting):
                self.shooting = False
                if (now - self.timeStartedShooting >= self.timeShooting+3000):
                    self.moving = True


    def move(self):
        self.rect.x += self.dx      # move to the new x-coord

    def shoot(self):
        now = pygame.time.get_ticks()
        if (now - self.lastShot > self.shotDelay):
            fire = Fire(self.rect.centerx, self.rect.y)
            Utils.allSprites.add(fire)
            self.fires.add(fire)
            self.lastShot = pygame.time.get_ticks()

    def setNewX(self):
        self.newX = self.generateNewX()
        # go right(1.0) if on left side... go left(-1.0) if on right side
        if self.rect.x < self.newX:
            self.dx = self.velocity*1.0
        else:
            self.dx = self.velocity*-1.0

    def generateNewX(self):
        min = self.width//2
        max = Utils.windowWidth - self.width
        print(min, max)
        return random.randrange(min, max)
    
    def getFires(self):
        return self.fires

    def getX(self):
        return self.rect.x

    def getY(self):
        return self.rect.x

    def getNewX(self):
        return self.newX

class Fire(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.radius = 25

        self.image = Utils.bowserFire
        self.image = pygame.transform.scale(self.image, (self.radius, self.radius))
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.velocity = 3.0
        self.dy = self.velocity*1.0
    
    def update(self):
        self.rect.y += self.dy