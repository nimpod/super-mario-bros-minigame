import pygame
from os import path

pygame.mixer.init()

FPS = 60
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 600
TITLE = "Danger, Bob-Omb!"

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

''' SETUP ASSETS FOLDERS '''
imgFolder = path.join(path.dirname(__file__), "res\img")
sndFolder = path.join(path.dirname(__file__), "res\snd")
style1 = path.join(imgFolder, "style1")
style2 = path.join(imgFolder, "style2")


''' LOAD IN IMAGES '''
background_img = pygame.image.load(path.join(imgFolder, "background.png")).convert()
fireball_img =   pygame.image.load(path.join(imgFolder, "fireball.png")).convert()
bowser_img =     pygame.image.load(path.join(imgFolder, "bowser.png")).convert()
bowserFire_img = pygame.image.load(path.join(imgFolder, "bowser_fire.png")).convert()
bombdead_img =   pygame.image.load(path.join(imgFolder, "bombdead.png")).convert()

bombImages = []
for i in range(2):
    filename = 'bomb0{}.png'.format(i)
    bombImages.append(pygame.image.load(path.join(imgFolder, filename)).convert())

explosionImages = []
for i in range(9):
    filename = 'explosion0{}.png'.format(i)
    img = pygame.image.load(path.join(imgFolder, filename)).convert()
    img.set_colorkey((0,0,0))
    explosionImages.append(img)

''' LOAD IN SOUND / MUSIC '''
pygame.mixer.music.load(path.join(sndFolder, 'menu_music.wav'))
pygame.mixer.music.set_volume(0.4)

playerSound = pygame.mixer.Sound(path.join(sndFolder, 'player_sound.wav'))
playerSound.set_volume(0.1)

playerExplosion = pygame.mixer.Sound(path.join(sndFolder, 'player_explosion.wav'))
playerExplosion.set_volume(0.9)


''' DRAWS TEXT TO SCREEN - you define the position, colour and font size of the text '''
def textToScreen(window, text, x, y, fontSize):
    text = str(text)
    font = pygame.font.SysFont('perpetua', fontSize)
    font.set_bold(True)
    text = font.render(text, True, (255,255,255))
    window.blit(text, (x,y))

''' PLAY MUSIC FILE '''
def playMusic(filename, volume):
    pygame.mixer.music.load(path.join(sndFolder, filename))
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play(loops=-1)


''' UTILITY CLASS FOR LOADING AND PARSING SPRITESHEETS '''
class Spritesheet:
    def __init__(self, filename):
        self.spritesheet = pygame.image.load(filename).convert()

    ''' get an image out of a larger spritesheet '''
    def get_image(self, x, y, width, height):
        image = pygame.Surface((width, height))
        image.blit(self.spritesheet, (0,0), (x,y,width,height))     # extract the image we want and blit to image surface
        return image