import pygame
import os, sys
import random
import math
import csv
import operator

import Player
import Fireball
from Utils import *
import Enemy

# Setup the game
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption(TITLE)
background_rect = background_img.get_rect()
background_img = pygame.transform.scale(background_img, (WINDOW_WIDTH, WINDOW_HEIGHT))

# Game state variables
gameOver = True
running = True

def update(window, allSprites):
    pygame.display.update()
    allSprites.update()

def render(window, allSprites):
    window.fill((0,0,0))        # reset background after each tick
    window.blit(background_img, background_rect)    
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
    window.blit(background_img, background_rect)

    # play the menu music
    playMusic('menu_music.wav', 0.4)

    # write text to screen
    textToScreen(window, "Danger Bob-Omb!", 35, WINDOW_HEIGHT/8 +10, 40)
    textToScreen(window, "Press any key to begin", WINDOW_WIDTH/4, WINDOW_HEIGHT - 20, 18)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit(0)
            if event.type == pygame.KEYUP:
                waiting = False
                playMusic('game_music.wav', 0.4)


''' GAME LOOP '''
while running:
    if gameOver:
        displayMainMenu()
        gameOver = False

        # initialise fireball variables
        fireballVelocity = 1.0
        maxFireballVelocity = 6.0
        numberOfFireballs = 3

        # initialise bowser-related variables
        firstShotTime = 0
        firstShot = True
        lastShot = pygame.time.get_ticks()
        collidedWithBowser = False
        timeShooting = 6000
        shotDelay = 150
        shootingAfterDelay = 3000

        # initialise game difficulty variables
        updateDifficulty = 7000
        lastGameDifficultyUpdate = 0

        # this tells us when the previous game ended, allowing us to calculate the player score accordingly
        lastgame = pygame.time.get_ticks()

        # pygame sprite group to hold all sprites in the game
        allSprites = pygame.sprite.Group()

        # Create the player and center them in middle of screen
        player1 = Player.Player(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + WINDOW_HEIGHT//4, "Nathan")
        player1.setScore(0)
        allSprites.add(player1)

        # Create the enemy Bowser
        bowser = Enemy.Enemy()
        allSprites.add(bowser)

        # Create group of fireballs
        fireballs = pygame.sprite.Group()
        for i in range (numberOfFireballs):
            f = Fireball.Fireball(fireballVelocity)
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
        if (keys[pygame.K_w]) and (player1.getY > WINDOW_HEIGHT//2):
            player1.moveUp()
        if (keys[pygame.K_s]) and (player1.getY < WINDOW_HEIGHT - player1.getHeight):
            player1.moveDown()
        if (keys[pygame.K_a]) and (player1.getX > 0):
            player1.moveLeft()
        if (keys[pygame.K_d]) and (player1.getX < WINDOW_WIDTH - player1.getWidth):
            player1.moveRight()
    else:
        player1.setMoving(False)
    
    ''' PLAYER ANIMATION '''
    updateEvery = 150               # waiting time until next player animation (milliseconds)
    player1.animate(updateEvery, pygame.time.get_ticks())

    update(window, allSprites)
    render(window, allSprites)


    ''' EVERY 7 SECONDS, UP THE LEVEL OF DIFFICULTY '''
    now = pygame.time.get_ticks()   # total run time of program (milliseconds)

    # increase difficulty of game...
    if (now - lastGameDifficultyUpdate >= updateDifficulty):
        # spawn a new fireball
        f = Fireball.Fireball(fireballVelocity)
        allSprites.add(f)
        fireballs.add(f)

        # increase the speed of each fireball
        fireballVelocity += 0.2
        if fireballVelocity < maxFireballVelocity:
            for fireball in fireballs:
                fireball.setVelocity(fireballVelocity)
        
        lastGameDifficultyUpdate = pygame.time.get_ticks()

    now = pygame.time.get_ticks()

    # print("moving(", bowser.getRectX() ,"-->",bowser.getNewX(), ") = ", bowser.getMoving(), " : shooting(", bowser.getRectX() ,") = ", bowser.getShooting(), " : ", bowser.direction())

    ''' BOWSER MOVEMENT '''
    # when bowser is not moving and not shooting find a new x-coord destination to move to
    if (not bowser.getMoving() and (not bowser.getShooting())):
        bowser.setNewX(bowser.generateNewX())
        bowser.setMoving(True)
        print("CHOOSING NEW X")

    #  when bowser if moving...
    if bowser.getMoving():
        bowser.move()

        # keep checking if bowser has reached its destination
        if (bowser.getRectX() == bowser.getNewX()):
            print("ARRIVED AT X(", bowser.getNewX(), ")")
            bowser.setMoving(False)
            bowser.setShooting(True)
            firstShotTime = pygame.time.get_ticks()

    # was it the first shot?
    if firstShot:
        firstShotTime = pygame.time.get_ticks()
    now = pygame.time.get_ticks()

    # bowser shoots for 'timeShooting' seconds...
    if (bowser.getShooting() and now - firstShotTime <= timeShooting):
        if (now - lastShot >= shotDelay or firstShot):
            f = Enemy.Fire(bowser.getRectX() + bowser.getWidth()//2.5, bowser.getRectY() +bowser.getHeight()//2.5)
            allSprites.add(f)
            bowserFires.add(f)
            lastShot = pygame.time.get_ticks()
            firstShot = False
    else:
        now = pygame.time.get_ticks()
        if (now - lastShot > shootingAfterDelay):
            bowser.setShooting(False)


    ''' DISPLAY CURRENT USER SCORE '''
    # calculate the current score
    score = int(pygame.time.get_ticks() - lastgame) / 16.7
    player1.setScore(score)

    # display the current score
    textToScreen(window, "Score", WINDOW_WIDTH - 125, 15, 15)
    textToScreen(window, player1.score, WINDOW_WIDTH - 15*(int(math.log10(player1.score))+1), 5, 25)


    ''' DISPLAY CURRENT HICSORE '''               
    hiscore = getHiScore(scores_dict)[1]
    textToScreen(window, "High Score", 15, 15, 15)        # write 'High Score' to screen
    textToScreen(window, str(hiscore), 100, 5, 25)        # write the current hiscore to screen

    # check if the current score is beating the hiscore
    if player1.score > hiscore:
        hiscore = int(player1.score)
        textToScreen(window, str(hiscore), 100, 5, 25)
    

    ''' GAME OVER '''
    fireballCollision = pygame.sprite.spritecollide(player1, fireballs, True, pygame.sprite.collide_circle)
    bowserFireCollision = pygame.sprite.spritecollide(player1, bowserFires, True, pygame.sprite.collide_circle)
    now = pygame.time.get_ticks()

    # when player collides with a fireball or bowsers fire...
    if (fireballCollision or bowserFireCollision) and not collidedWithBowser:
        print("DEAD")
        collidedWithBowser = True
        # player1.setImage(Utils.bombdead)

        # play explosion sound upon impact
        playerExplosion.play()
        
        # show explosion animation upon impact
        playerExplosionImg = Player.Explosion(player1.getCenter(), 1)
        allSprites.add(playerExplosionImg)     

        # remove the player from allSprites by killing them
        player1.kill()
    
    # after the explosion animation, then end the game
    if (not player1.alive() and (not playerExplosionImg.alive())):
        # write the players final score to the csv file
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
            textToScreen(window, str(fireball.getId()) + " (" + str(fireball.getX())+","+str(fireball.getY())+")", fireball.getX()-10, fireball.getY()-10, 13)

pygame.quit()