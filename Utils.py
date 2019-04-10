import pygame
from os import path

pygame.mixer.init()

FPS = 60
windowWidth = 400
windowHeight = 600
title = "Danger, Bob-Omb!"
fireballCounter = 5
fireballStartingVelocity = 1.0

window = pygame.display.set_mode((windowWidth, windowHeight))


''' SETUP ASSETS FOLDERS '''
imgFolder = path.join(path.dirname(__file__), "res\img")
sndFolder = path.join(path.dirname(__file__), "res\snd")
style1 = path.join(imgFolder, "style1")
style2 = path.join(imgFolder, "style2")


''' LOAD IN IMAGES '''
background = pygame.image.load(path.join(imgFolder, "background.png")).convert()
fireball = pygame.image.load(path.join(imgFolder, "fireball.png")).convert()
bowser = pygame.image.load(path.join(imgFolder, "bowser.png")).convert()

bombImages = []
bombImagesList = [ 'bomb1.png', 'bomb2.png' ]
for img in bombImagesList:
    bombImages.append(pygame.image.load(path.join(imgFolder, img)).convert())


''' LOAD IN SOUND / MUSIC '''
pygame.mixer.music.load(path.join(sndFolder, 'game_music.wav'))
pygame.mixer.music.set_volume(0.4)

playerSound = pygame.mixer.Sound(path.join(sndFolder, 'player_sound.wav'))
playerSound.set_volume(0.1)

playerExplosion = pygame.mixer.Sound(path.join(sndFolder, 'player_explosion.wav'))
playerExplosion.set_volume(0.9)



# Function to draw to text to the screen. You define the position, colour and font size of the text
def textToScreen(window, text, x, y, fontColor, fontSize):
    text = str(text)
    font = pygame.font.SysFont('perpetua', fontSize)
    font.set_bold(True)
    text = font.render(text, True, fontColor)
    window.blit(text, (x,y))