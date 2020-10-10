from settings import BLUE, CELLWIDTH, CELLHEIGHT, HEIGHTBUFFER

import pygame

class Wall:
    """ xPos = 0
    yPos = 0
    location = [xPos,yPos]
    gridPos = [] """

    def __init__(self, view, location):
        self.view = view
        self.location = location
        self.xPos = location[0]
        self.yPos = location[1]
        self.gridPos = [ self.xPos//CELLWIDTH , self.yPos//CELLHEIGHT ]

    def draw(self):
        self.rect = pygame.Rect(self.xPos,self.yPos,CELLWIDTH,CELLHEIGHT)
        pygame.draw.rect(self.view.screen, BLUE, self.rect)