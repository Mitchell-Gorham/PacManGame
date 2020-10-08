from interactableClass import *
from movementClass import *
from settings import *
import pygame

class Ghost(Movement):
    personality = ''    # Valid personalities are the integers: 0 (Inky), 1 (Blinky), 2 (Pinky), 3 (Clyde)
    state = ''          # Valid States are: inactive, active, flee, dead, alternate
    colour = [RED, PINK, CYAN, ORANGE]

    def __init__(self, view, personality, state):
        self.view = view
        self.personality = personality
        self.state = state
        
    def draw(self):
        pygame.draw.circle(self.view.screen, self.colourFunc(), (self.xPos, self.yPos),10)

    def colourFunc(self):
        if self.state == 'flee':
            return BLUE
        else:
            return self.colour[self.personality]