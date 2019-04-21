import pygame
import os, sys
import random
import math
import csv
import operator
import pandas as pd

import Player
import Fireball
import Enemy
from Utils import *

# pygame initilisation
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.init()
pygame.mixer.init()

clock = pygame.time.Clock()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# set window information
pygame.display.set_caption(TITLE)
background_rect = background_img.get_rect()
background_img = pygame.transform.scale(background_img, (WINDOW_WIDTH, WINDOW_HEIGHT))
# spritesheet = Spritesheet(os.path.join(imgFolder, SPRITESHEET))

# Buttons
x = WINDOW_WIDTH//3
y = WINDOW_HEIGHT//1.7
w = 130
h = 30
start_button = Button(x, y, w, h, WHITE, 'START')
settings_button = Button(x, (y+(h*2)), w, h, WHITE, 'SETTINGS')
scores_button = Button(x, (y+(h*4)), w, h, WHITE, 'SCORES')
exit_button = Button(x, (y+(h*6)), w, h, WHITE, 'EXIT')
buttons = [start_button, settings_button, scores_button, exit_button]

# Game state variables
game_over = True
running = True
startup = True
paused = False
game_state = 'MAIN MENU'

def update(window, all_sprites):
    pygame.display.update()
    all_sprites.update()

def render(window, all_sprites):
    window.fill(BLACK)        # reset background after each tick
    window.blit(background_img, background_rect)    
    all_sprites.draw(window)

def redraw_buttons(window):
    for b in buttons:
        b.draw(window, BLACK)

def quit():
    pygame.quit()
    sys.exit(0)

''' WHEN PLAYER STARTS GAME OR EXITS GAME OVER SCREEN, THIS MAIN MENU SCREEN IS DISPLAYED '''
def display_main_menu():
    game_state = 'MAIN MENU'
    print(game_state)

    # refresh the background
    window.blit(background_img, background_rect)
    redraw_buttons(window)

    # play the menu music
    play_music('menu_music.wav', VOLUME)

    # write text to screen
    text_to_screen(window, "Danger Bob-Omb!", 35, WINDOW_HEIGHT/8 +10, 40)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            # player presses 'x' button
            if event.type == pygame.QUIT:
                running = False
                quit()
            
            # button interaction
            for b in buttons:
                # player clicks a button
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if b.is_over(pos):
                        if b.__repr__() == 'START':
                            waiting = False
                            play_music('game_music.wav', VOLUME)
                        elif b.__repr__() == 'SETTINGS':
                            print('you clicked the settings button')
                        elif b.__repr__() == 'SCORES':
                            print('you clicked the sccores button')
                        elif b.__repr__() == 'EXIT':
                            running = False
                            quit()
                # player hovers over a button
                if event.type == pygame.MOUSEMOTION:
                    if b.is_over(pos):
                        b.color = GREEN
                    else:
                        b.color = WHITE


''' WHEN PLAYER DIES THIS FUNCTION IS CALLED TO DISPLAY GAME OVER RELATED INFORMATION '''
def display_game_over_screen():
    game_state = 'GAME OVER'
    print(game_state)

    # append the username and score to csv
    append_score(SCORES_CSV, str(player1.username), int(player1.score))
    
    # read csv as dataframe
    df = pd.read_csv(SCORES_CSV)

    # sort dataframe by scores
    df = df.sort_values('score', ascending=False)

    player_pos = 0
    for index,row in df.iterrows():
        if row['username'] == str(player1.username) and row['score'] == int(player1.score):
            player_pos = index+1
            break

    firstPlace = df.iloc[0]['score']
    tenthPlace = df.iloc[9]['score']

    text = ''
    if int(player1.score) == firstPlace:
        play_music('game_over_1st_music.wav', VOLUME)
        text = 'New Hiscore! Oh my god Becky!'
    elif int(player1.score) < tenthPlace:
        play_music('game_over_not_top10_music.wav', VOLUME)
    elif int(player1.score) >= tenthPlace:
        play_music('game_over_top10_music.wav', VOLUME)
        text = 'Congrats, you got top 10!'

    # create an input box for user to type their name
    box = InputBox(WINDOW_WIDTH//4 +10, WINDOW_HEIGHT//2.4 +32, 140, 32)

    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                change_username("unnamed-user")
                running = False
                quit()
            elif event.type == pygame.KEYUP and event.key == pygame.K_RETURN:
                done = True
            box.handle_event(event)
        box.update()
        render(window, all_sprites)

        # display stuff on screen
        h = WINDOW_HEIGHT//1.67
        w = WINDOW_WIDTH//3.5

        # text to tell the user to type in their name
        text_to_screen(window, "Please type your name in the box below", WINDOW_WIDTH//7.6, WINDOW_HEIGHT//2.3, 18)

        # additional feedback
        text_to_screen(window, text, WINDOW_WIDTH//5, h -30, 20)

        # display top 10 scores
        i = 0
        for index, row in df.iterrows():
            if str(row['username']) == 'you' and int(row['score']) == int(player1.score):
                colour = GREEN
            else:
                colour = WHITE
            # display pos, username, score
            text_to_screen(window, str(i+1)            , w   , h+(i*18), 15, colour)
            text_to_screen(window, str(row['username']), w+40, h+(i*18), 15, colour)
            text_to_screen(window, str(row['score'])   , w+160, h+(i*18), 15, colour)
            i += 1
            if i == 10:
                break
        # show the pos, username, score if user didn't get in top 10
        if int(player1.score) < tenthPlace:
            text_to_screen(window, str('--------------------------------'), w, WINDOW_HEIGHT//1.11, 15)
            text_to_screen(window, str(player_pos), w, WINDOW_HEIGHT//1.08, 15, RED)
            text_to_screen(window, str(player1.username), w+40, WINDOW_HEIGHT//1.08, 15, RED)
            text_to_screen(window, str(int(player1.score)), w+160, WINDOW_HEIGHT//1.08, 15, RED)

        box.draw(window)

        pygame.display.flip()
        clock.tick(30)
    
    change_username(str(player1.username))

    display_main_menu()

''' UPDATE USERNAME OF A DATA ENTRY IN CSV FILE '''
def change_username(username):
    df = pd.read_csv(SCORES_CSV)        # re-read the csv into a dataframe
    df.drop(df.tail(1).index,inplace=True)                          # delete the most recent row
    df.to_csv(SCORES_CSV, encoding='utf-8', index=False)    # write updated dataframe to csv

    # re-append with new username
    append_score(SCORES_CSV, username, int(player1.score))


''' APPEND A USERNAME & SCORE TO CSV '''
def append_score(filename, username, score):
    # write the players final score to the csv file
    with open(filename, 'a', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow([username, score])


COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
FONT = pygame.font.Font(None, 32)

class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):       # If the user clicked on the input_box rect.
                self.active = not self.active           # Toggle the active variable.
            else:
                self.active = False
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE        # Change the current color of the input box.
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    player1.setUsername(self.text)
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)

    def getText(self):
        return self.text

    def update(self):
        width = max(200, self.txt_surface.get_width()+10)       # Resize the box if the text is too long.
        self.rect.w = width

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))   # Blit the text.
        pygame.draw.rect(screen, self.color, self.rect, 2)              # Blit the rect.

''' GAME LOOP '''
while running:
    if startup:
        display_main_menu()
    elif game_over:
        display_game_over_screen()
    
    if game_over or startup:
        game_state = 'GAME ACTIVE'

        startup = False
        game_over = False

        # initialise fireball variables
        fireball_vel = 1.0
        max_fireball_vel = 6.0
        num_fireballs = 4

        # initialise bowser-related variables
        first_shot_time = 0
        first_shot = True
        last_shot = pygame.time.get_ticks()
        collidedWithBowser = False
        time_shooting = 6000
        shot_delay = 150
        after_shot_delay = 3000

        # initialise game difficulty variables
        update_difficulty = 6000
        last_difficulty_update = 0

        # this tells us when the previous game ended, allowing us to calculate the player score accordingly
        last_game = pygame.time.get_ticks()

        # pygame sprite group to hold all sprites in the game
        all_sprites = pygame.sprite.Group()

        # Create the player and center them in middle of screen
        player1 = Player.Player(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + WINDOW_HEIGHT//4, "you")
        player1.setScore(0)
        all_sprites.add(player1)

        # Create the enemy Bowser
        bowser = Enemy.Enemy()
        all_sprites.add(bowser)

        # Create group of fireballs
        fireballs = pygame.sprite.Group()
        for i in range (num_fireballs):
            f = Fireball.Fireball(fireball_vel)
            all_sprites.add(f)
            fireballs.add(f)

        # create group of fires for Bowser
        bowser_fires = pygame.sprite.Group()

        # load scores.csv into a dictionary
        df = pd.read_csv(SCORES_CSV)

    clock.tick(FPS)
    pygame.event.pump()

    for event in pygame.event.get():
        # player presses 'x' button
        if event.type == pygame.QUIT:
            running = False
            quit()
        
        # player moves using mouse
        if event.type == pygame.MOUSEMOTION:
            mx, my = pygame.mouse.get_pos()
            if (my > WINDOW_HEIGHT//2) and (my < WINDOW_HEIGHT - player1.getHeight) and (mx > 0) and (mx < WINDOW_WIDTH - player1.getWidth):
                player1.setX(mx)
                player1.setY(my)

        if event.type == pygame.KEYDOWN:
            # player presses 'esc' key
            if event.key == pygame.K_ESCAPE:
                running = False
                quit()
            # player presses 'p' to pause game
            if event.key == pygame.K_p:
                paused = not(paused)

    ''' PLAYER MOVEMENT - keyboard '''
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
    player1.animate(pygame.time.get_ticks())

    update(window, all_sprites)
    render(window, all_sprites)

    ''' EVERY 7 SECONDS, UP THE LEVEL OF DIFFICULTY '''
    now = pygame.time.get_ticks()
    if (now - last_difficulty_update >= update_difficulty):
        # spawn a new fireball
        f = Fireball.Fireball(fireball_vel)
        all_sprites.add(f)
        fireballs.add(f)

        # increase the speed of each fireball
        fireball_vel += 0.1
        if fireball_vel < max_fireball_vel:
            for fireball in fireballs:
                fireball.setVelocity(fireball_vel)
        
        last_difficulty_update = pygame.time.get_ticks()

    now = pygame.time.get_ticks()

    # print("moving(", bowser.getRectX() ,"-->",bowser.getNewX(), ") = ", bowser.getMoving(), " : shooting(", bowser.getRectX() ,") = ", bowser.getShooting(), " : ", bowser.direction())

    ''' BOWSER MOVEMENT '''
    # when bowser is not moving and not shooting find a new x-coord destination to move to
    if (not bowser.getMoving() and (not bowser.getShooting())):
        bowser.setNewX(bowser.generateNewX())
        bowser.setMoving(True)
        # print("CHOOSING NEW X")

    #  when bowser if moving...
    if bowser.getMoving():
        bowser.move()

        # keep checking if bowser has reached its destination
        if (bowser.getRectX() == bowser.getNewX()):
            # print("ARRIVED AT X(", bowser.getNewX(), ")")
            bowser.setMoving(False)
            bowser.setShooting(True)
            first_shot_time = pygame.time.get_ticks()

    # was it the first shot?
    if first_shot:
        first_shot_time = pygame.time.get_ticks()
    now = pygame.time.get_ticks()

    # bowser shoots for 'time_shooting' seconds...
    if (bowser.getShooting() and now - first_shot_time <= time_shooting):
        if (now - last_shot >= shot_delay or first_shot):
            f = Enemy.Fire(bowser.getRectX() + bowser.getWidth()//2.5, bowser.getRectY() +bowser.getHeight()//2.5)
            all_sprites.add(f)
            bowser_fires.add(f)
            last_shot = pygame.time.get_ticks()
            first_shot = False
    else:
        now = pygame.time.get_ticks()
        if (now - last_shot > after_shot_delay):
            bowser.setShooting(False)
    
    # delete a fire from all_sprites if it is off the screen
    for f in bowser_fires:
        if (f.getY() > WINDOW_HEIGHT):
            f.kill()


    ''' DISPLAY CURRENT USER SCORE '''
    # re-calculate the current score, but only when player is alive
    if (player1.alive()):
        score = int(pygame.time.get_ticks() - last_game) / 16.7
        player1.setScore(score)

    # display the current score
    text_to_screen(window, "Score", WINDOW_WIDTH - 125, 15, 15)
    text_to_screen(window, player1.score, WINDOW_WIDTH - 15*(int(math.log10(player1.score))+1), 5, 25)


    ''' DISPLAY CURRENT HICSORE '''
    df_copy = df.sort_values('score', ascending=False)
    hiscore = int(df_copy.iloc[0,1])
    text_to_screen(window, "High Score", 15, 15, 15)        # write 'High Score' to screen
    if player1.score > hiscore:
        hiscore = int(player1.score)
        text_to_screen(window, str(hiscore), 100, 5, 25)
    else:
        text_to_screen(window, str(hiscore), 100, 5, 25)        # write the current hiscore to screen   

    ''' GAME OVER '''
    fireballCollision = pygame.sprite.spritecollide(player1, fireballs, True, pygame.sprite.collide_circle)
    bowserFireCollision = pygame.sprite.spritecollide(player1, bowser_fires, True, pygame.sprite.collide_circle)
    now = pygame.time.get_ticks()

    # when player collides with a fireball or bowsers fire...
    if (fireballCollision or bowserFireCollision) and not collidedWithBowser:
        game_state = 'DEAD'
        collidedWithBowser = True
        player1.setImage(bombdead_img)

        # play explosion sound upon impact
        playerExplosion.play()
        
        # show explosion animation upon impact
        playerExplosionImg = Player.Explosion(player1.getCenter(), 1)
        all_sprites.add(playerExplosionImg)     

        # remove the player from all_sprites by killing them
        player1.kill()
    
    # after the explosion animation, then end the game
    if (not player1.alive() and (not playerExplosionImg.alive())):
        game_over = True

    ''' DEBUGGING '''
    # print(pygame.font.get_fonts())        # print out all font types in pygame!
    if (keys[pygame.K_SPACE]):
        for fireball in fireballs:
            text_to_screen(window, str(fireball.getId()) + " (" + str(fireball.getX())+","+str(fireball.getY())+")" + ":" + str(fireball.getVelocity()), fireball.getX()-10, fireball.getY()-10, 13)

pygame.quit()