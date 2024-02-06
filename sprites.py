import pygame
import constants as c

#============================================================================


class SpriteSheet(object):

    def __init__(self, file_name):
        self.sprite_sheet = pygame.image.load(file_name).convert_alpha()

    def getImage(self, x, y, width, height):
        image = pygame.Surface([width, height]).convert()
        image.blit(self.sprite_sheet, (0,0), (x, y, width, height))
        image.set_colorkey(c.White)
        return image

#shipSprite1 : x =   0, y =   0, width = 110, height = 110
#shipSprite2 : x = 110, y =   0, width = 110, height = 110
#eLaser      : x = 220, y =   0, width =   6, height =  47
#pLaser      : x = 220, y =  47, width =   6, height =  47
#asteroid    : x = 248, y =   0, width =  25, height =  25
#astBreak1   : x = 273, y =   0, width =  25, height =  25
#astBreak2   : x = 298, y =   0, width =  25, height =  25
#astBreak3   : x = 423, y =   0, width =  25, height =  25
#astCrack1   : x = 248, y =  25, width =  25, height =  25
#astCrack2   : x = 273, y =  25, width =  25, height =  25
#astCrack3   : x = 298, y =  25, width =  25, height =  25
#enemyShip1  : x =   0, y = 110, width = 111, height = 111
#enemyShip2  : x = 111, y = 110, width = 111, height = 111
    
#============================================================================



