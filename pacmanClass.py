from movementClass import *
from settings import YELLOW
import pygame

class PacMan(Movement):
    state = ''         # Valid states are: inactive, active, powerup, dead
    
    def __init__(self, view, state):
        self.view = view
        self.state = state

    def draw(self):
        pygame.draw.circle(self.view.screen, YELLOW, (self.xPos, self.yPos),10)
        