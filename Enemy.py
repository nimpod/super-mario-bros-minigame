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
        self.shotDelay = 175
        self.timeShooting = 5000
        self.timeStartedShooting = pygame.time.get_ticks()

    def update(self):
        # move bowser if he's not moving or shooting
        if (self.shooting == False and self.moving == False):
            self.moving = True
            self.setNewX()

        # keep moving bowser...
        if (self.moving == True):
            self.move()
            self.timeStoppedMoving = pygame.time.get_ticks()
            print("BOWSER MOVING FROM ", self.rect.x, " to ", self.newX)
            # until he reaches the new x-coord
            if (self.rect.x == self.newX):
                self.moving = False
                self.shooting = True
                self.timeStartedShooting = pygame.time.get_ticks()
        
        # 3 seconds after moving, shoot, then stop for 3 seconds
        now = pygame.time.get_ticks()
        if (self.shooting == True and now - self.timeStoppedMoving >= 1000):
            self.shoot()
            print("BOWSER SHOOTING")
            if (now - self.timeStartedShooting >= self.timeShooting):
                self.shooting = False
                print("BOWSER STOP SHOOTING")
                self.moving = True
                self.setNewX()

    def move(self):
        if (self.rect.x > -60 and self.rect.x < Utils.windowWidth +60):
            self.rect.x += self.dx      # move to the new x-coord

    def shoot(self):
        now = pygame.time.get_ticks()
        if (now - self.lastShot > self.shotDelay):
            f = Fire(self.rect.centerx -10, self.rect.y +70)
            Utils.allSprites.add(f)
            Utils.bowserFires.add(f)
            self.lastShot = pygame.time.get_ticks()

    def setNewX(self):
        self.newX = self.generateNewX()
        # go right(1.0) if on left side... go left(-1.0) if on right side
        if self.rect.x < self.newX:
            self.dx = self.velocity*1.0
        else:
            self.dx = self.velocity*-1.0

    def generateNewX(self):
        min = self.width//4
        max = Utils.windowWidth - self.width//1.6
        return random.randrange(min, max)

    def getX(self):
        return self.rect.x

    def getY(self):
        return self.rect.x

    def getNewX(self):
        return self.newX

class Fire(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.radius = 30

        self.orig_image = Utils.bowserFire
        self.orig_image = pygame.transform.scale(self.orig_image, (self.radius, self.radius))
        self.orig_image.set_colorkey((255,255,255))
        self.image = self.orig_image.copy()
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
        '''self.rotate()
        self.enlarge()
        '''
        
    def rotate(self):
        now = pygame.time.get_ticks()
        # every 50ms...
        if (now - self.lastUpdate >= 50):
            self.lastUpdate = now
            self.rotationAngle = (self.rotationAngle + self.rotationVelocity) % 360         # loop the angle back to 0 when it reaches 360
            new_image = pygame.transform.rotate(self.orig_image, self.rotationVelocity)    # rotate the fire
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center
    
    def enlarge(self):
        self.radius += 1