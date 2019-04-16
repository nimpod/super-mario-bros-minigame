import pygame
import os
import Utils
import random
import itertools

class Fireball(pygame.sprite.Sprite):

    idGenerator = itertools.count(1)            # generate unique ID for each fireball

    def __init__(self):
        self.id = next(self.idGenerator)
        self.radius = 13

        pygame.sprite.Sprite.__init__(self)
        self.image = Utils.fireball
        self.image = pygame.transform.scale(self.image, (self.radius, self.radius))
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()

        # pygame.draw.circle(self.image, (0,0,0), self.rect.center, self.radius)    # Draw the players hitbox
        
        self.quadrantXY = self.chooseRandomQuadrant(random.choice(self.quadrants))
        self.velocity = Utils.fireballStartingVelocity

        self.respawn()


    def chooseRandomQuadrant(self, randomQuadrant):
        if (randomQuadrant == "UPPER"):
            return (random.randrange(0.0, Utils.windowWidth),random.randrange(Utils.windowHeight/2.0 - self.radius*2, Utils.windowHeight/2.0), random.choice([-1,1]), 1.0)
        elif (randomQuadrant == "RIGHT"):
            return (random.randrange(Utils.windowWidth, Utils.windowWidth + self.radius*2), random.randrange(0, Utils.windowHeight), -1.0, random.choice([-1,1]))
        elif (randomQuadrant == "LOWER"):
            return (random.randrange(0.0, Utils.windowWidth), random.randrange(Utils.windowHeight, Utils.windowHeight + self.radius*2), random.choice([-1,1]), -1.0)
        elif (randomQuadrant == "LEFT"):
            return (random.randrange(0.0 - (self.radius*2), 0.0), random.randrange(0, Utils.windowHeight), 1.0, random.choice([-1,1]))
    

    def respawn(self):
        self.quadrantXY = self.chooseRandomQuadrant(random.choice(self.quadrants))

        self.rect.x = self.quadrantXY[0]
        self.rect.y = self.quadrantXY[1]
        self.dx = self.quadrantXY[2]*self.velocity
        self.dy = self.quadrantXY[3]*self.velocity
    

    def update(self):
        self.rect.y += self.dy
        self.rect.x += self.dx

        if (self.rect.top > Utils.windowHeight+self.radius*2) or (self.rect.bottom < Utils.windowHeight/2.0 -self.radius*2) or (self.rect.right < -self.radius*2) or (self.rect.left > Utils.windowWidth+self.radius*2):
            self.respawn()

    @property
    def quadrants(self):
        return [ "UPPER", "RIGHT", "LOWER", "LEFT" ]

    def getX(self):
        return self.rect.x
    
    def getY(self):
        return self.rect.y

    def getVelocity(self):
        return self.velocity

    def getId(self):
        return self.id

    def setVelocity(self, newVelocity):
        self.velocity = newVelocity

    def __repr__(self):
        return '({},{})'.format(self.rect.x, self.rect.y)