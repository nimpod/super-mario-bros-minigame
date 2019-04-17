def gameLoop(window, running):
    fireballVelocity = Utils.fireballStartingVelocity

    scores_dict = updateScoresDict()    

    pygame.mixer.music.play(loops=-1)

    while running:
        clock.tick(FPS)
        pygame.event.pump()
        
        ''' PLAYER MOVEMENT '''
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_w] or keys[pygame.K_s] or keys[pygame.K_a] or keys[pygame.K_d]):
            Utils.playerMoving = True
        else:
            Utils.playermoving = False
        
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
        if (now - last >= gap):         # if 7 seconds have passed and bowser is not moving...
            # spawn a new fireball
            f = Fireball.Fireball()
            allSprites.add(f)
            fireballs.add(f)

            # increase the speed of each fireball
            fireballVelocity += 0.1
            if fireballVelocity < 5.0:
                for fireball in fireballs:
                    fireball.setVelocity(fireballVelocity)
            
            last = pygame.time.get_ticks()

        ''' DISPLAY SCORE INFORMATION '''
        # write current player score to screen
        player1.setScore(int(pygame.time.get_ticks()) / 16.7)
        scoreLen = int(math.log10(player1.score))+1

        Utils.textToScreen(window, "Score", windowWidth - 125, 15, 15)
        Utils.textToScreen(window, player1.score, windowWidth - 15*scoreLen, 5, 25)

        # write hiscore to screen
        hiscore = getHiScore(scores_dict)[1]
        hiscoreLen = int(math.log10(hiscore))+1

        if player1.score > hiscore:
            hiscore = int(player1.score)

        Utils.textToScreen(window, "High Score", 15, 15, 15)
        Utils.textToScreen(window, str(hiscore), 100, 5, 25)
        

        ''' END GAME '''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


        ''' GAME OVER '''
        fireballCollision = pygame.sprite.spritecollide(player1, fireballs, False, pygame.sprite.collide_circle)
        bowserFireCollision = pygame.sprite.spritecollide(player1, bowserFires, False, pygame.sprite.collide_circle)

        if (fireballCollision or bowserFireCollision):
            Utils.playerExplosion.play()            
            with open('super-mario-bros-minigame/scores.csv', 'a', newline='') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow([str(player1.username), int(player1.score)])

            # printScores(scores_dict)                  # print out the scores_dict row-by-row
            running = False


        ''' DEBUGGING '''
        # print(pygame.font.get_fonts())        # print out all font types in pygame!

        if (keys[pygame.K_SPACE]):
            for fireball in fireballs:
                Utils.textToScreen(window, str(fireball.getId()) + " (" + str(fireball.getX())+","+str(fireball.getY())+")", fireball.getX()-10, fireball.getY()-10, 13)



def update(window, allSprites):
    pygame.display.update()
    allSprites.update()


def render(window, allSprites):
    window.fill((0,0,0))        # reset background after each tick
    window.blit(background, background_rect)    
    allSprites.draw(window)


''' PRE-LOAD or UPDATE THE LIST OF SCORES FROM THE scores.csv FILE '''
def updateScoresDict():
    inputfile = csv.DictReader(open("super-mario-bros-minigame/scores.csv"))
    scores_dict = []
    for row in inputfile:
        scores_dict.append(row)
    
    return scores_dict


''' GET HIGH SCORE FROM scores.csv '''
def getHiScore(scores_dict):
    hiscore = None
    username = None
    for row in scores_dict:
        current_username = str(row['username'])
        current_score = int(row['score'])
        if (hiscore == None) or (current_score >= hiscore):
            hiscore = current_score
            username = current_username

    return (username, hiscore)


def getTopN():
    data = csv.reader(open('super-mario-bros-minigame/scores.csv'), delimiter=',')
    return sorted(data, key=int(operator.itemgetter(1)))    # 0 specifies according to first column we want to sort

''' PRINT OUT THE SCORES '''
def printScores(scores_dict):
    for row in scores_dict:
        print(row['username'], row['score'])        


import pygame
import os
import random
import math
import csv
import operator

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
allSprites = Utils.allSprites
bowserFires = Utils.bowserFires

# Setup the game
pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()
pygame.display.set_caption(title)
background_rect = background.get_rect()
background = pygame.transform.scale(background, (windowWidth, windowHeight))

# Create the player and center them in middle of screen
player1 = Player.Player(windowWidth//2, windowHeight//2 + windowHeight//4, "Nathan")
allSprites.add(player1)

# Create the enemy Bowser
bowser = Enemy.Enemy()
allSprites.add(bowser)

# Create group of fireballs
fireballs = pygame.sprite.Group()
for i in range (numberOfFireballs):
    f = Fireball.Fireball()
    allSprites.add(f)
    fireballs.add(f)

bowserFires = pygame.sprite.Group()

# Run the game
running = True
gameLoop(window, running)
pygame.quit()