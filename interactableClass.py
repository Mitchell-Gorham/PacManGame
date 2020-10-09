from settings import RED, CYAN, PINK, ORANGE, WHITE, YELLOW, BLACK, CELLWIDTH, CELLHEIGHT

import pygame

class Interactable:
    interactableType = ''    # Valid types are: d (dot), p (powerpellet), + more for fruits
    #C(herry)=100, S(trawberry)=300, O(range)=500, A(pple)=700, M(elon)=1000, G(alaxian)=2000, B(ell)=3000, K(ey)=5000
    interactableValue = [10, 50, 100, 300, 500, 700, 1000, 2000, 5000]
    score = 0
    xPos = 0
    yPos = 0
    location = [xPos,yPos]
    gridPos = []

    def __init__(self, view, location, interactableType):
        self.view = view
        self.location = location
        self.xPos = location[0]
        self.yPos = location[1]
        self.gridPos = [ self.xPos//CELLWIDTH , self.yPos//CELLHEIGHT ]
        self.interactableType = interactableType
        self.score = self.interactableValue[interactableType]

    def remove(self, interactList, value):    # Visually remove this thing
        interactList.pop(value)

    def draw(self):
        if self.interactableType == 0:
            pygame.draw.circle(self.view.screen, YELLOW, (self.xPos, self.yPos),3)
        elif self.interactableType == 1:
            pygame.draw.circle(self.view.screen, YELLOW, (self.xPos, self.yPos),5)
        elif self.interactableType == 2:
            pygame.draw.circle(self.view.screen, RED, (self.xPos, self.yPos),8)
        else:
            pygame.draw.circle(self.view.screen, CYAN, (self.xPos, self.yPos),10)