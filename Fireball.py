import pygame
import os
import Utils
import random

class Fireball(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10,10))
        self.image.fill((255,0,0))
        self.rect = self.image.get_rect()

        self.rect.x, self.rect.y = random.randrange(0.0, Utils.windowWidth), random.randrange(250.0, 300.0)
        
        self.velocity = 1.0
        self.dy = self.velocity
        self.dx = random.choice([self.velocity*-1, self.velocity])

    def respawn(self):
        self.rect.x, self.rect.y = random.randrange(0.0, Utils.windowWidth), random.randrange(250.0, 300.0)
        
    def update(self):
        self.rect.y += self.dy
        self.rect.x += self.dx
        
        if (self.rect.top > Utils.windowHeight+10 or self.rect.left < -10 or self.rect.right > Utils.windowWidth+10):
            self.respawn()
    
    def setX(self, newX):
        this.rect.x = newX
    
    def setY(self, newY):
        this.rect.y = newY
