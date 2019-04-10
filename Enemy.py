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
        self.rect.center = (Utils.windowWidth//1.85, Utils.windowHeight//6)

        self.velocity = 3
        self.dx = self.velocity
        self.dy = self.velocity

    def shoot(self):
        print("BOWSER SHOOT")

    def move(self):
        newX = random.randrange(self.width//2, Utils.windowWidth - self.width//2)
        self.dx = 1.0 if (self.rect.x < newX) else -1.0         # go right(1.0) if on left side... go left(-1.0) if on right side
        print(newX, " : ", self.dx)
        if (self.rect.x != newX):
            self.rect.x += self.dx