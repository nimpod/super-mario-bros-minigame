import pygame as pg
from pygame import surface
from os import path

pg.mixer.init()

FPS = 60
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 600
TITLE = "Danger, Bob-Omb!"
VOLUME = 0.9
SCORES_CSV = 'super-mario-bros-minigame/scores.csv'
SPRITESHEET = "spritesheet_1.png"
SPRITESHEET_2 = "spritesheet_2.png"

window = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

''' SETUP ASSETS FOLDERS '''
imgFolder = path.join(path.dirname(__file__), "res\img")
sndFolder = path.join(path.dirname(__file__), "res\snd")

''' LOAD IN SOUND / MUSIC '''
# menu music
pg.mixer.music.load(path.join(sndFolder, 'menu_music.wav'))
pg.mixer.music.set_volume(0.4)

# game sounds
playerSound = pg.mixer.Sound(path.join(sndFolder, 'player_sound.wav'))
playerSound.set_volume(0.1)

playerExplosion = pg.mixer.Sound(path.join(sndFolder, 'player_explosion.wav'))
playerExplosion.set_volume(0.9)

enemyFire = pg.mixer.Sound(path.join(sndFolder, 'enemy_fire.wav'))
enemyFire.set_volume(0.05)

countdown = pg.mixer.Sound(path.join(sndFolder, 'countdown.wav'))
countdown.set_volume(0.9)

''' DRAWS TEXT TO SCREEN - you define the position, colour and font size of the text '''
def text_to_screen(window, text, x, y, size, colour=(255,255,255), family='perpetua'):
    text = str(text)
    font = pg.font.SysFont(family, size)
    font.set_bold(True)
    text = font.render(text, True, colour)
    window.blit(text, (x,y))

''' PLAY MUSIC FILE '''
def play_music(filename, volume):
    pg.mixer.music.load(path.join(sndFolder, filename))
    pg.mixer.music.set_volume(volume)
    pg.mixer.music.play(loops=-1)

def play_sound_once(filename, volume):
    pg.mixer.music.load(path.join(sndFolder, filename))
    pg.mixer.music.set_volume(volume)
    pg.mixer.music.play()

''' COLOURS '''
BLACK = (0,0,0)
GREEN = (240,255,0)
PINK = (255,192,203)
RED = (255,0,0)
WHITE = (255,255,255)

''' UTILITY CLASS FOR LOADING AND PARSING SPRITESHEETS '''
class Spritesheet:
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()

    ''' get an image out of a larger spritesheet '''
    def get_image(self, x, y, width, height):
        image = surface.Surface((width, height))
        image.blit(self.spritesheet, (0,0), (x,y,width,height))     # extract the image we want and blit to image surface
        return image

spritesheet = Spritesheet(path.join(imgFolder, SPRITESHEET))
''' LOAD IN IMAGES '''
fireball_img = spritesheet.get_image(152, 402, 26, 26)
enemy_fire_img = spritesheet.get_image(152, 380, 25, 22)
enemy_img = spritesheet.get_image(0, 380, 152, 117)
if STYLE == '1':
    background_img = spritesheet.get_image(0, 0, 253, 380)
    bombImages = [spritesheet.get_image(199, 380, 16, 25), spritesheet.get_image(215, 380, 16, 25), spritesheet.get_image(231, 380, 22, 32)]
elif STYLE == '2':
    background_img = spritesheet.get_image(0, 0, 253, 380)
    bombImages = [spritesheet.get_image(229, 402, 23, 23), spritesheet.get_image(205, 402, 23, 23), spritesheet.get_image(205, 402, 23, 23)]


explosionImages = []
for i in range(9):
    filename = 'explosion0{}.png'.format(i)
    img = pg.image.load(path.join(imgFolder, filename)).convert()
    img.set_colorkey((0,0,0))
    explosionImages.append(img)


''' UTILITY CLASS FOR CREATING INTERACTIVE BUTTONS '''
class Button:
    def __init__(self, x, y, width, height, colour, text=''):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.colour = colour
        self.text = text
    
    def draw(self, window, outline=None):
        if outline:
            pg.draw.rect(window, self.colour, (self.x-2, self.y-2, self.width+4, self.height+4), 0)
        pg.draw.rect(window, self.colour, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font = pg.font.SysFont('perpetua', 20)
            text = font.render(self.text, 1, BLACK)
            window.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))
    
    def is_over(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
        return False

    def __repr__(self):
        return self.text

class MenuSprite(pg.sprite.Sprite):
    def __init__(self, imgarray, x, y, width, height, updateAnimation):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.imgarray = imgarray
        
        self.imagenum = 1
        self.oldTime = 0
        self.updateAnimation = updateAnimation

        pg.sprite.Sprite.__init__(self)
        self.setImage(self.imgarray[self.imagenum])

        self.rect = self.image.get_rect()
        self.radius = (self.width+self.height)//10
        self.rect.center = (x,y)

    def update(self):
        self.animate(pg.time.get_ticks())
        self.move()

    def animate(self, totalTime):
        if (totalTime - self.oldTime >= self.updateAnimation):
            if (self.imagenum == 0):
                self.imagenum = 1
            elif (self.imagenum == 1):
                self.imagenum = 0            
            self.setImage(self.imgarray[self.imagenum])
            self.oldTime = totalTime
        
    def move(self):
        self.x -= 1.0

    def setImage(self, newImg):
        self.image = pg.transform.scale(newImg, (self.width, self.height))
        self.image.set_colorkey(WHITE)

    def getX(self):
        return self.x