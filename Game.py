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
windowWidth = Utils.windowWidth
windowHeight = Utils.windowHeight
FPS = Utils.FPS
title = Utils.title
background = Utils.background
numberOfFireballs = Utils.fireballCounter

# Setup the game
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()
window = pygame.display.set_mode((windowWidth, windowHeight))
pygame.display.set_caption(title)
background_rect = background.get_rect()
background = pygame.transform.scale(background, (windowWidth, windowHeight))

# Game state variables
gameOver = True
running = True

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

''' GET THE TOP N SCORES FROM scores.csv '''
def getTopN():
    data = csv.reader(open('super-mario-bros-minigame/scores.csv'), delimiter=',')
    return sorted(data, key=int(operator.itemgetter(1)))    # 0 specifies according to first column we want to sort

''' PRINT OUT THE SCORES '''
def printScores(scores_dict):
    for row in scores_dict:
        print(row['username'], row['score'])

''' DISPLAY THE MAIN MENU SCREEN '''
def displayMainMenu():
    print("MAIN MENU")

    # refresh the background
    window.blit(background, background_rect)

    # play the menu music
    Utils.playMusic('menu_music.wav', 0.4)

    # write text to screen
    Utils.textToScreen(window, "Danger Bob-Omb!", 35, windowHeight/8 +10, 40)
    Utils.textToScreen(window, "Press any key to begin", windowWidth/4, windowHeight - 20, 18)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False
                Utils.playMusic('game_music.wav', 0.4)


''' GAME LOOP '''
while running:
    if gameOver:
        displayMainMenu()
        gameOver = False

        # other game setup things
        fireballVelocity = Utils.fireballStartingVelocity
        firstShotTime = 0
        firstShot = True
        lastShot = pygame.time.get_ticks()
        collidedWithBowser = False
        lastGameDifficultyUpdate = 0

        # this tells us when the previous game ended, allowing us to calculate the player score accordingly
        lastgame = pygame.time.get_ticks()

        # pygame sprite group to hold all sprites in the game
        allSprites = pygame.sprite.Group()

        # Create the player and center them in middle of screen
        player1 = Player.Player(windowWidth//2, windowHeight//2 + windowHeight//4, "Nathan")
        player1.setScore(0)
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

        # create group of fires for Bowser
        bowserFires = pygame.sprite.Group()

        # load scores.csv into a dictionary
        scores_dict = updateScoresDict()

    clock.tick(FPS)
    pygame.event.pump()
    
    ''' PLAYER MOVEMENT '''
    keys = pygame.key.get_pressed()
    if player1.alive() and (keys[pygame.K_w] or keys[pygame.K_s] or keys[pygame.K_a] or keys[pygame.K_d]):
        player1.setMoving(True)
        if (keys[pygame.K_w]) and (player1.getY > windowHeight//2):
            player1.moveUp()
        if (keys[pygame.K_s]) and (player1.getY < windowHeight - player1.getHeight):
            player1.moveDown()
        if (keys[pygame.K_a]) and (player1.getX > 0):
            player1.moveLeft()
        if (keys[pygame.K_d]) and (player1.getX < windowWidth - player1.getWidth):
            player1.moveRight()
    else:
        player1.setMoving(False)
    
    ''' PLAYER ANIMATION '''
    updateEvery = 150   # waiting time until next player animation (milliseconds)
    player1.animate(updateEvery, pygame.time.get_ticks())

    update(window, allSprites)
    render(window, allSprites)


    ''' EVERY 7 SECONDS, UP THE LEVEL OF DIFFICULTY '''
    gap = 7000                      # waiting time until next level of difficulty (milliseconds)
    now = pygame.time.get_ticks()   # total run time of program (milliseconds)

    if (now - lastGameDifficultyUpdate >= gap):         # if 7 seconds have passed and bowser is not moving...
        # spawn a new fireball
        f = Fireball.Fireball()
        allSprites.add(f)
        fireballs.add(f)

        # increase the speed of each fireball
        fireballVelocity += 0.2
        if fireballVelocity < 5.0:
            for fireball in fireballs:
                fireball.setVelocity(fireballVelocity)
        
        lastGameDifficultyUpdate = pygame.time.get_ticks()

    now = pygame.time.get_ticks()

    #print("moving(", bowser.getRectX() ,"-->",bowser.getNewX(), ") = ", bowser.getMoving(), " : shooting(", bowser.getRectX() ,") = ", bowser.getShooting(), " : ", bowser.direction())

    ''' BOWSER MOVEMENT '''
    # if bowser is not moving and not shooting
    if (not bowser.getMoving() and (not bowser.getShooting())):
        bowser.setNewX(bowser.generateNewX())
        bowser.setMoving(True)
        print("CHOOSING NEW X")
    
    if bowser.getMoving():
        bowser.move()

        # if bowser is moving and reached its destination
        if (bowser.getRectX() == bowser.getNewX()):
            print("ARRIVED AT X(", bowser.getNewX(), ")")
            bowser.setMoving(False)
            bowser.setShooting(True)
            firstShotTime = pygame.time.get_ticks()

    if firstShot:
        firstShotTime = pygame.time.get_ticks()
    now = pygame.time.get_ticks()
    timeShooting = 6000
    shotDelay = 150

    # bowser shoots
    if (bowser.getShooting() and now - firstShotTime <= timeShooting):
        if (now - lastShot >= shotDelay or firstShot):
            f = Enemy.Fire(bowser.getRectX() +   bowser.getWidth()//2.5, bowser.getRectY() +bowser.getHeight()//2.5)
            allSprites.add(f)
            bowserFires.add(f)
            lastShot = pygame.time.get_ticks()
            firstShot = False
    else:
        now = pygame.time.get_ticks()
        if (now - lastShot > 3000):
            bowser.setShooting(False)


    ''' DISPLAY SCORE INFORMATION '''
    # write current player score to screen
    score = int(pygame.time.get_ticks() - lastgame) / 16.7

    player1.setScore(score)
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


    ''' GAME OVER '''
    fireballCollision = pygame.sprite.spritecollide(player1, fireballs, True, pygame.sprite.collide_circle)
    bowserFireCollision = pygame.sprite.spritecollide(player1, bowserFires, True, pygame.sprite.collide_circle)

    now = pygame.time.get_ticks()

    if (fireballCollision or bowserFireCollision) and not collidedWithBowser:
        print("DEAD")
        collidedWithBowser = True

        player1.setImage(Utils.bombdead)            # use the bombdead sprite instead
        Utils.playerExplosion.play()                # play the explosion sound
        
        playerExplosionImg = Player.Explosion(player1.getCenter(), 1)         # show explosion
        allSprites.add(playerExplosionImg)     

        player1.kill()
    
    if (not player1.alive() and (not playerExplosionImg.alive())):
        with open('super-mario-bros-minigame/scores.csv', 'a', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow([str(player1.username), int(player1.score)])
        # printScores(scores_dict)                  # print out the scores_dict row-by-row
        
        gameOver = True

    ''' PRESS x BUTTON '''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    ''' DEBUGGING '''
    # print(pygame.font.get_fonts())        # print out all font types in pygame!
    if (keys[pygame.K_SPACE]):
        for fireball in fireballs:
            Utils.textToScreen(window, str(fireball.getId()) + " (" + str(fireball.getX())+","+str(fireball.getY())+")", fireball.getX()-10, fireball.getY()-10, 13)