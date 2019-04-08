import pygame
import os


FPS = 60
windowWidth = 400
windowHeight = 600
title = "Danger, Bob-Omb!"
fireballCounter = 20
fireballStartingVelocity = 1.0

window = pygame.display.set_mode((windowWidth, windowHeight))

# Assets setup
gameFolder = os.path.dirname(__file__)
imgFolder = os.path.join(gameFolder, "res\img")
style1 = os.path.join(imgFolder, "style1")
style2 = os.path.join(imgFolder, "style2")

# Assets from res/img folder
background = pygame.image.load(os.path.join(imgFolder, "background.png")).convert()
fireball = pygame.image.load(os.path.join(imgFolder, "fireball.png")).convert()

bombImages = []
bombImagesList = [ 'bomb1.png', 'bomb2.png' ]
for img in bombImagesList:
    bombImages.append(pygame.image.load(os.path.join(imgFolder, img)).convert())


## Draw to text to the screen. You define the position, colour and font size of the text
def textToScreen(window, text, x, y, fontColor, fontSize):
    text = str(text)
    font = pygame.font.SysFont(None, fontSize)
    text = font.render(text, True, fontColor)
    window.blit(text, (x,y))