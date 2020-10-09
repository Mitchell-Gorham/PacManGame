from movementClass import Movement
from settings import DEBUG, RED, CYAN, PINK, ORANGE, BLUE, WHITE, PLAYERRADIUS, CELLWIDTH, CELLHEIGHT
import pygame

class Ghost(Movement):
    personality = ''    # Valid personalities are the integers: 0 (Blinky), 1 (Pinky), 2 (Inky), 3 (Clyde)
    state = ''          # Valid States are: inactive, chase, scatter, flee, dead
    colour = [RED, PINK, CYAN, ORANGE]
    targetGrid = [0,0]
    nextGrid = [0,0]
    gridList = []
    xTar = 0
    yTar = 0


    def __init__(self, controller, personality, state):
        self.controller = controller
        self.personality = personality
        self.state = state
        
        self.scatterGrid = self.getScatterGrid()

    def draw(self):
        if self.state == 'dead':
            pygame.draw.circle(self.controller.screen, WHITE, (self.xPos-6, self.yPos), PLAYERRADIUS//3)
            pygame.draw.circle(self.controller.screen, WHITE, (self.xPos+6, self.yPos), PLAYERRADIUS//3)
        else:
            pygame.draw.circle(self.controller.screen, self.colourFunc(), (self.xPos, self.yPos), PLAYERRADIUS)

    def colourFunc(self):
        if self.state == 'flee':
            return BLUE
        else:
            return self.colour[self.personality]

    def setFlee(self):
        if self.state != 'dead':
            self.state = 'flee'

    def getScatterGrid(self):    # replace with CELL stuff to allow for game size changes
        if self.personality == 0:
            return [26,2]
        elif self.personality == 1:
            return [1,2]
        elif self.personality == 2:
            return [26,34]
        elif self.personality == 3:
            return [1,34]
        return [14,14]
    
    def getTarget(self, controller, x, y):
        # DO STUFF HERE
        return [controller.player.gridPos[0]+x, controller.player.gridPos[1]+y]

    def personalityFunc(self, controller):
        # Default state - Ghosts act according to their personality
        if self.state == 'chase':
            # Blinky - Personality
            if self.personality == 0:    # Blinky aims for the player's current grid pos
                self.xTar, self.yTar = 0, 0
                self.targetGrid = self.getTarget(controller, self.xTar, self.yTar)

                """
                get current grid
                get current direction
                get next grid
                Draw line to target grid positon
                check grids adjacent to next grid
                pick grid closest that places self closest to target grid
                """ 
            # Pinky - Personality
            elif self.personality == 1:  # Pinky aims for the player's current grid pos + 4 in their current dir
                if controller.player.currentDirection == 'N':
                    self.xTar = 0
                    self.yTar = -4
                elif controller.player.currentDirection == 'E':
                    self.xTar = 4
                    self.yTar = 0
                elif controller.player.currentDirection == 'S':
                    self.xTar = 0
                    self.yTar = 4
                elif controller.player.currentDirection == 'W':
                    self.xTar = -4
                    self.yTar = 0
                else:
                    self.xTar = 0
                    self.yTar = 0

                self.targetGrid = self.getTarget(controller, self.xTar, self.yTar)

            #Inky - Personality
            elif self.personality == 2:  # Inky uses the player's current location as well as Blinky's to hunt
                if controller.player.currentDirection == 'N':
                    self.xTar = 0
                    self.yTar = -2
                elif controller.player.currentDirection == 'E':
                    self.xTar = 2
                    self.yTar = 0
                elif controller.player.currentDirection == 'S':
                    self.xTar = 0
                    self.yTar = 2
                elif controller.player.currentDirection == 'W':
                    self.xTar = -2
                    self.yTar = 0
                else:
                    self.xTar = 0
                    self.yTar = 0


                self.targetGrid = self.getTarget(controller, self.xTar, self.yTar)
            
            # Clyde - Personality
            elif self.personality == 3:
                self.xTar, self.yTar = 0, 0
                self.targetGrid = self.getTarget(controller, self.xTar, self.yTar)
                if (self.gridPos[0] - 8 <= self.targetGrid[0] <= self.gridPos[0] + 8) or (self.gridPos[1] - 8 <= self.targetGrid[1] <= self.gridPos[1] + 8):
                    self.targetGrid = self.scatterGrid
            
        # Second state - Ghosts enter this state at set intervals
        elif self.state == 'scatter':
            self.targetGrid = self.scatterGrid
            # Blinky heads to the NE corner
            # Pinky heads to the NW coner
            # Inky heads to the SE corner
            # Clyde heads to the SW corner

        elif self.state == 'flee':
            pass

        elif self.state == 'dead':
            self.targetGrid = [ self.spawnPos[0]//CELLWIDTH , self.spawnPos[1]//CELLHEIGHT ]
            if self.gridPos == self.targetGrid:
                self.state == 'chase'

        self.getNextMove(controller, self.targetGrid)

    def getNextMove(self, controller, targetGrid):
        
        if self.currentDirection == 'N':
            if not any(wall.gridPos == [self.gridPos[0],self.gridPos[1]-1] for wall in controller.walls):
                self.nextGrid = [self.gridPos[0],self.gridPos[1]-1]
            for x in range(-1, 2, 1):
                if x in (-1, 1):
                    if not any(wall.gridPos == [self.nextGrid[0]+x,self.nextGrid[1]] for wall in controller.walls):
                        self.gridList.append([self.nextGrid[0]+x,self.nextGrid[1]])
                if x == 0:
                    if not any(wall.gridPos == [self.nextGrid[0],self.nextGrid[1]-1] for wall in controller.walls):
                        self.gridList.append([self.nextGrid[0],self.nextGrid[1]-1])
        
        elif self.currentDirection == 'E':
            if not any(wall.gridPos == [self.gridPos[0]+1,self.gridPos[1]] for wall in controller.walls):
                self.nextGrid = [self.gridPos[0]+1,self.gridPos[1]]
            for y in range(-1, 2, 1):
                if y in (-1, 1):
                    if not any(wall.gridPos == [self.nextGrid[0],self.nextGrid[1]+y] for wall in controller.walls):
                        self.gridList.append([self.nextGrid[0],self.nextGrid[1]+y])
                if y == 0:
                    if not any(wall.gridPos == [self.nextGrid[0]+1,self.nextGrid[1]] for wall in controller.walls):
                        self.gridList.append([self.nextGrid[0]+1,self.nextGrid[1]])

        elif self.currentDirection == 'S':
            if not any(wall.gridPos == [self.gridPos[0],self.gridPos[1]+1] for wall in controller.walls):
                self.nextGrid = [self.gridPos[0],self.gridPos[1]+1]
            for x in range(-1, 2, 1):
                if x in (-1, 1):
                    if not any(wall.gridPos == [self.nextGrid[0]+x,self.nextGrid[1]] for wall in controller.walls):
                        self.gridList.append([self.nextGrid[0]+x,self.nextGrid[1]])
                if x == 0:
                    if not any(wall.gridPos == [self.nextGrid[0],self.nextGrid[1]+1] for wall in controller.walls):
                        self.gridList.append([self.nextGrid[0],self.nextGrid[1]+1])

        elif self.currentDirection == 'W':
            if not any(wall.gridPos == [self.gridPos[0]-1,self.gridPos[1]] for wall in controller.walls):
                self.nextGrid = [self.gridPos[0]-1,self.gridPos[1]]
            for y in range(-1, 2, 1):
                if y in (-1, 1):
                    if not any(wall.gridPos == [self.nextGrid[0],self.nextGrid[1]+y] for wall in controller.walls):
                        self.gridList.append([self.nextGrid[0],self.nextGrid[1]+y])
                if y == 0:
                    if not any(wall.gridPos == [self.nextGrid[0]-1,self.nextGrid[1]] for wall in controller.walls):
                        self.gridList.append([self.nextGrid[0]-1,self.nextGrid[1]])

        #use self.gridList to determine self.nextDirection based on self.targetGrid

        if not DEBUG:   # if not in debug mode, clean out list here instead of after they're drawn
            self.gridList = []
