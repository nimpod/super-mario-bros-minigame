import pygame
import os


FPS = 60
windowWidth = 400
windowHeight = 600
title = "Danger, Bob-Omb!"

window = pygame.display.set_mode((windowWidth, windowHeight))

# Assets setup
gameFolder = os.path.dirname(__file__)
imgFolder = os.path.join(gameFolder, "res\img")
style1 = os.path.join(imgFolder, "style1")
style2 = os.path.join(imgFolder, "style2")

# Assets from res/img folder
background = pygame.image.load(os.path.join(imgFolder, "background.png")).convert()

bombImages = []
bombImagesList = [ 'bomb1.png', 'bomb2.png' ]
for img in bombImagesList:
    bombImages.append(pygame.image.load(os.path.join(imgFolder, img)).convert())

# fireball = pygame.image.load(os.path.join(imgFolder, "fireball.png")).convert()