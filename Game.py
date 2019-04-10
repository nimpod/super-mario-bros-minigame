def gameLoop(window, running):
    fireballVelocity = Utils.fireballStartingVelocity

    pygame.mixer.music.play(loops=-1)

    while running:
        clock.tick(FPS)

        ''' END GAME '''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        ''' GAME OVER '''
        playerDied = pygame.sprite.spritecollide(player1, fireballs, False, pygame.sprite.collide_circle)
        if (playerDied):
            Utils.playerExplosion.play()
            running = False
        
        ''' PLAYER MOVEMENT '''
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_w]) and (player1.getY > windowHeight//2):
            player1.moveUp()
        if (keys[pygame.K_s]) and (player1.getY < windowHeight - player1.getHeight):
            player1.moveDown()
        if (keys[pygame.K_a]) and (player1.getX > 0):
            player1.moveLeft()
        if (keys[pygame.K_d]) and (player1.getX < windowWidth - player1.getWidth):
            player1.moveRight()

        ''' PLAYER ANIMATION '''
        updateEvery = 150   # waiting time until next player animation (milliseconds)
        player1.animate(updateEvery, pygame.time.get_ticks())

        update(window, allSprites)
        render(window, allSprites)

        ''' EVERY 7 SECONDS, UP THE LEVEL OF DIFFICULTY '''
        gap = 7000                      # waiting time until next level of difficulty (milliseconds)
        now = pygame.time.get_ticks()   # total run time of program (milliseconds)
        if (now < gap):
            last = 0
        if (now - last >= gap):
            # spawn a new fireball
            f = Fireball.Fireball()
            allSprites.add(f)
            fireballs.add(f)

            # increase the speed of each fireball
            fireballVelocity += 0.1
            for fireball in fireballs:
                fireball.setVelocity(fireballVelocity)
            
            # move Bowser
            bowser.move()
            bowser.shoot()
            
            last = pygame.time.get_ticks()


        ''' SHOW AND UPDATE PLAYER SCORE '''
        player1.setScore(int(pygame.time.get_ticks()) / 16.7)
        scoreLen = int(math.log10(player1.score))+1

        # draw all score-related text at the top of screen
        Utils.textToScreen(window, "Score", windowWidth - 125, 15, (255,255,255), 15)
        Utils.textToScreen(window, player1.score, windowWidth - 15*scoreLen, 5, (255,255,255), 25)

        Utils.textToScreen(window, "High Score", 15, 15, (255,255,255), 15)
        # Utils.textToScreen(window, player1.score, windowWidth - 15*scoreLen, 15, (255,255,255), 35)


        # Debugging
        if (keys[pygame.K_SPACE]):
            for fireball in fireballs:
                Utils.textToScreen(window, str(fireball.getId()) + " (" + str(fireball.getX())+","+str(fireball.getY())+")", fireball.getX()-10, fireball.getY()-10, (255,255,255), 13)



def update(window, allSprites):
    pygame.display.update()
    allSprites.update()


def render(window, allSprites):
    window.fill((0,0,0))        # reset background after each tick
    window.blit(background, background_rect)
    allSprites.draw(window)


import pygame
import os
import random
import math

import Player
import Fireball
import Utils
import Enemy

# Get variables from Utils.py
window = Utils.window
windowWidth = Utils.windowWidth
windowHeight = Utils.windowHeight
FPS = Utils.FPS
title = Utils.title
background = Utils.background
numberOfFireballs = Utils.fireballCounter

# Setup the game
pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()

pygame.display.set_caption(title)
allSprites = pygame.sprite.Group()

background_rect = background.get_rect()
background = pygame.transform.scale(background, (windowWidth, windowHeight))


# Create the player and center them in middle of screen
player1 = Player.Player(windowWidth//2, windowHeight//2 + windowHeight//4)
allSprites.add(player1)

# Create group of fireballs
fireballs = pygame.sprite.Group()
for i in range (numberOfFireballs):
    f = Fireball.Fireball()
    allSprites.add(f)
    fireballs.add(f)

# Create the enemy Bowser
bowser = Enemy.Enemy()
allSprites.add(bowser)

# print(pygame.font.get_fonts())

# Run the game
running = True
gameLoop(window, running)
pygame.quit()
