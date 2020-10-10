from movementClass import Movement
from settings import YELLOW, PLAYERRADIUS, CELLHEIGHT, CELLWIDTH, HEIGHTBUFFER, STYLE
import pygame

class PacMan(Movement):   
    
    def __init__(self, controller, state):
        super().__init__()
        self.controller = controller
        self.state = state  # Valid states are: inactive, active, dead
        self.speed = 3

    def draw(self):
        if STYLE:
            pygame.draw.circle(self.controller.screen, YELLOW, (self.gridPos[0]*CELLHEIGHT+(CELLHEIGHT//2), self.gridPos[1]*CELLWIDTH+(CELLWIDTH//2)),PLAYERRADIUS)
        else:
            pygame.draw.circle(self.controller.screen, YELLOW, (self.xPos, self.yPos),PLAYERRADIUS)
        