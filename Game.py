def gameLoop(window, running):
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        if (keys[pygame.K_w]) and (player1.getY > windowHeight//2 + player1.getWidth):
            player1.moveUp()
        if (keys[pygame.K_s]) and (player1.getY < windowHeight-player1.getHeight*1.5):
            player1.moveDown()
        if (keys[pygame.K_a]) and (player1.getX > player1.getWidth):
            player1.moveLeft()
        if (keys[pygame.K_d]) and (player1.getX < windowWidth-player1.getWidth*1.5):
            player1.moveRight()

        updateEvery = 250   # miliseconds
        player1.animate(updateEvery, pygame.time.get_ticks())

        playerDied = pygame.sprite.spritecollide(player1, fireballs, False, pygame.sprite.collide_circle)
        if (playerDied):
            running = False

        update(window, allSprites)
        render(window, allSprites)


def update(window, allSprites):
    pygame.display.update()
    allSprites.update()


def render(window, allSprites):
    window.fill((0,0,0))        # reset background after each tick
    window.blit(background, background_rect)
    allSprites.draw(window)



import pygame
import os
import Utils
import Player
import Fireball

# Get variables from Utils.py
window = Utils.window
windowWidth = Utils.windowWidth
windowHeight = Utils.windowHeight
FPS = Utils.FPS
title = Utils.title
background = Utils.background


# Setup the game
pygame.init()
clock = pygame.time.Clock()

pygame.display.set_caption(title)
allSprites = pygame.sprite.Group()

background_rect = background.get_rect()
background = pygame.transform.scale(background, (windowWidth, windowHeight))


# Create the player and center them in middle of screen
player1 = Player.Player(windowWidth//2, windowHeight//2 + windowHeight//4)

# add player1 to the sprites
allSprites.add(player1)

# Create a group of fireballs
numberOfFireballs = 30
fireballs = pygame.sprite.Group()
for i in range (numberOfFireballs):
    f = Fireball.Fireball()
    allSprites.add(f)
    fireballs.add(f)


# Run the game
running = True
gameLoop(window, running)
pygame.quit()
