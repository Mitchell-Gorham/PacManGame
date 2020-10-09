from movementClass import Movement
from settings import *
import pygame

class Ghost(Movement):
    personality = ''    # Valid personalities are the integers: 0 (Blinky), 1 (Pinky), 2 (Inky), 3 (Clyde)
    state = ''          # Valid States are: inactive, chase, scatter, flee, dead, alternate
    colour = [RED, CYAN, PINK, ORANGE]
    targetGrid = []
    scatterGrid = []


    def __init__(self, controller, personality, state):
        self.controller = controller
        self.personality = personality
        self.state = state
        
        self.scatterGrid = self.getScatterLoc()

    def draw(self):
        pygame.draw.circle(self.controller.screen, self.colourFunc(), (self.xPos, self.yPos), PLAYERRADIUS)

    def colourFunc(self):
        if self.state == 'flee':
            return BLUE
        else:
            return self.colour[self.personality]

    def setFlee(self):
        self.state = 'flee'

    def getScatterLoc(self):    # replace with CELL stuff to allow for game size changes
        if self.personality == 0:
            return [26,2]
        elif self.personality == 1:
            return [1,2]
        elif self.personality == 2:
            return [26,34]
        elif self.personality == 3:
            return [1,34]
        return [14,14]

    def personalityFunc(self, controller, personality, state):
        # Blinky - Personality
        if personality == 0:
            if state == 'chase':   # Blinky aims for the player's current grid pos
                self.targetGrid = controller.player.gridPos      
            elif state == 'scatter':
                self.targetGrid = self.scatterGrid

        # Pinky - Personality
        elif personality == 1:
            if state == 'chase':   # Pinky aims for the player's current grid pos + 4 in their current dir
                self.targetGrid = controller.player.gridPos + [4,0]
            elif state == 'scatter':
                self.targetGrid = self.scatterGrid

        # Inky - Personality
        elif personality == 2:
            if state == 'chase':   # Pac-Man's tile dir + 2, Blinky's offset from that time x2 is target
                self.targetGrid = controller.player.gridPos + [2,0] # controller.ghost[0].gridPos
            elif state == 'scatter':
                self.targetGrid = self.scatterGrid

        # Clyde - Personality
        elif personality == 3:
            # Clyde 
            if state == 'chase':    # Goes after player like Blinky, unless he's less than 8 cells away
                self.targetGrid = controller.player.gridPos
            elif state == 'alternate':  # Runs to scatterGrid location if pacman is within 8 tiles
                self.targetGrid = self.scatterGrid
            elif state == 'scatter':
                self.targetGrid = self.scatterGrid
