from settings import BLUE, WHITE, CELLWIDTH, CELLHEIGHT, HEIGHTBUFFER

import pygame

class Wall:
    def __init__(self, view, location, wallType):
        self.view = view
        self.location = location
        self.wallType = wallType
        self.xPos = location[0]
        self.yPos = location[1]
        self.gridPos = [ self.xPos//CELLWIDTH , self.yPos//CELLHEIGHT ]

    def draw(self):
        if self.wallType == 'w':
            self.rect = pygame.Rect(self.xPos,self.yPos,CELLWIDTH,CELLHEIGHT)
            pygame.draw.rect(self.view.screen, BLUE, self.rect)
        elif self.wallType == '_':
            self.rect = pygame.Rect(self.xPos,self.yPos+6,CELLWIDTH,CELLHEIGHT//2-1)
            pygame.draw.rect(self.view.screen, WHITE, self.rect)