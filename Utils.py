import pygame
from os import path

pygame.mixer.init()

FPS = 60
windowWidth = 400
windowHeight = 600
title = "Danger, Bob-Omb!"
fireballCounter = 3
fireballStartingVelocity = 1.0
window = pygame.display.set_mode((windowWidth, windowHeight))
allSprites = pygame.sprite.Group()
bowserFires = pygame.sprite.Group()
playermoving = False


''' SETUP ASSETS FOLDERS '''
imgFolder = path.join(path.dirname(__file__), "res\img")
sndFolder = path.join(path.dirname(__file__), "res\snd")
style1 = path.join(imgFolder, "style1")
style2 = path.join(imgFolder, "style2")


''' LOAD IN IMAGES '''
background = pygame.image.load(path.join(imgFolder, "background.png")).convert()
fireball =   pygame.image.load(path.join(imgFolder, "fireball.png")).convert()
bowser =     pygame.image.load(path.join(imgFolder, "bowser.png")).convert()
bowserFire = pygame.image.load(path.join(imgFolder, "bowser_fire.png")).convert()

bombImages = []
bombImagesList = [ 'bomb01.png', 'bomb02.png' ]
for img in bombImagesList:
    bombImages.append(pygame.image.load(path.join(imgFolder, img)).convert())
    
bombdead = pygame.image.load(path.join(imgFolder, "bombdead.png")).convert()


''' LOAD IN SOUND / MUSIC '''
pygame.mixer.music.load(path.join(sndFolder, 'game_music.wav'))
pygame.mixer.music.set_volume(0.4)

playerSound = pygame.mixer.Sound(path.join(sndFolder, 'player_sound.wav'))
playerSound.set_volume(0.1)

playerExplosion = pygame.mixer.Sound(path.join(sndFolder, 'player_explosion.wav'))
playerExplosion.set_volume(0.9)


# Function to draw to text to the screen. You define the position, colour and font size of the text
def textToScreen(window, text, x, y, fontSize):
    text = str(text)
    font = pygame.font.SysFont('perpetua', fontSize)
    font.set_bold(True)
    text = font.render(text, True, (255,255,255))
    window.blit(text, (x,y))