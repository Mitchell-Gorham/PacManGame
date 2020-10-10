from settings import RED, CYAN, PINK, ORANGE, WHITE, YELLOW, BLACK, CELLWIDTH, CELLHEIGHT
import pygame

class Interactable:
    #C(herry)=100, S(trawberry)=300, O(range)=500, A(pple)=700, M(elon)=1000, G(alaxian)=2000, B(ell)=3000, K(ey)=5000
    interactableValue = [10, 50, 100, 300, 500, 700, 1000, 2000, 5000]

    def __init__(self, controller, location, interactableType):
        self.controller = controller
        self.location = location
        self.xPos = location[0]
        self.yPos = location[1]
        self.gridPos = [ self.xPos//CELLWIDTH , self.yPos//CELLHEIGHT ]
        self.interactableType = interactableType
        self.score = self.interactableValue[interactableType]

    def draw(self):
        if self.interactableType == 0:
            pygame.draw.circle(self.controller.screen, YELLOW, (self.xPos, self.yPos),3)
        elif self.interactableType == 1:
            pygame.draw.circle(self.controller.screen, YELLOW, (self.xPos, self.yPos),5)
        elif self.interactableType == 2:
            pygame.draw.circle(self.controller.screen, RED, (self.xPos+1, self.yPos+1),8)
        else:
            pygame.draw.circle(self.controller.screen, CYAN, (self.xPos, self.yPos),10)

    def remove(self, interactList, value):
        interactList.pop(value)

class Fruit(Interactable):

    def __init__(self, controller, location, interactableType, timer):
        super().__init__(controller, location, interactableType)
        self.timer = timer

    def timerTick(self):
        self.timer -= 1
        if self.timer <= 0:
            return True
        else:
            return False