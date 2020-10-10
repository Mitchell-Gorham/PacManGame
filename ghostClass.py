from movementClass import Movement
from settings import DEBUG, STYLE, RED, CYAN, PINK, ORANGE, BLUE, WHITE, PLAYERRADIUS, CELLWIDTH, CELLHEIGHT
from math import hypot
import pygame

class Ghost(Movement):
    colour = [RED, PINK, CYAN, ORANGE]

    def __init__(self, controller, personality, state):
        super().__init__()
        self.controller = controller
        self.personality = personality  # Valid personalities are the integers: 0 (Blinky), 1 (Pinky), 2 (Inky), 3 (Clyde)
        self.state = state              # Valid States are: inactive, chase, scatter, flee, dead
        
        self.scatterGrid = self.getScatterGrid()
        self.gridList = []
        self.targetGrid = [0,0]
        self.xTar = 0
        self.yTar = 0
        self.nextGrid = [0,0]

    def draw(self):
        if STYLE:
            if self.state == 'dead':
                pygame.draw.circle(self.controller.screen, WHITE, (self.gridPos[0]*CELLHEIGHT+(CELLHEIGHT//2)-6, self.gridPos[1]*CELLWIDTH+(CELLWIDTH//2)-2), PLAYERRADIUS//3)
                pygame.draw.circle(self.controller.screen, WHITE, (self.gridPos[0]*CELLHEIGHT+(CELLHEIGHT//2)+6, self.gridPos[1]*CELLWIDTH+(CELLWIDTH//2)-2), PLAYERRADIUS//3)
            else:
                
                pygame.draw.circle(self.controller.screen, self.colourFunc(), (self.gridPos[0]*CELLHEIGHT+(CELLHEIGHT//2), self.gridPos[1]*CELLWIDTH+(CELLWIDTH//2)), PLAYERRADIUS)
                pygame.draw.circle(self.controller.screen, WHITE, (self.gridPos[0]*CELLHEIGHT+(CELLHEIGHT//2)-6, self.gridPos[1]*CELLWIDTH+(CELLWIDTH//2)-2), PLAYERRADIUS//3)
                pygame.draw.circle(self.controller.screen, WHITE, (self.gridPos[0]*CELLHEIGHT+(CELLHEIGHT//2)+6, self.gridPos[1]*CELLWIDTH+(CELLWIDTH//2)-2), PLAYERRADIUS//3)
        else:
            if self.state == 'dead':
                pygame.draw.circle(self.controller.screen, WHITE, (self.xPos-6, self.yPos-2), PLAYERRADIUS//3)
                pygame.draw.circle(self.controller.screen, WHITE, (self.xPos+6, self.yPos-2), PLAYERRADIUS//3)
            else:
                
                pygame.draw.circle(self.controller.screen, self.colourFunc(), (self.xPos, self.yPos), PLAYERRADIUS)
                pygame.draw.circle(self.controller.screen, WHITE, (self.xPos-6, self.yPos-2), PLAYERRADIUS//3)
                pygame.draw.circle(self.controller.screen, WHITE, (self.xPos+6, self.yPos-2), PLAYERRADIUS//3)

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
    
    def getTarget(self, origin, x, y):
        # DO STUFF HERE
        return [origin[0]+x, origin[1]+y]

    def personalityFunc(self, controller):
        # Default state - Ghosts act according to their personality
        if self.state == 'chase':
            # Blinky - Personality
            if self.personality == 0:    # Blinky aims for the player's current grid pos
                self.xTar, self.yTar = 0, 0
                self.targetGrid = self.getTarget(controller.player.gridPos, self.xTar, self.yTar)

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

                self.targetGrid = self.getTarget(controller.player.gridPos, self.xTar, self.yTar)

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

                # offset 2 ahead of pacman, get distance of RED to this offset, double it, there's your target x,y offsets

                self.xTar = controller.ghosts[0].gridPos[0]-controller.player.gridPos[0]+self.xTar
                self.yTar = controller.ghosts[0].gridPos[1]-controller.player.gridPos[1]+self.yTar

                

                self.targetGrid = self.getTarget(controller.player.gridPos, self.xTar, self.yTar)


            
            # Clyde - Personality
            elif self.personality == 3:
                self.xTar, self.yTar = 0, 0
                self.targetGrid = self.getTarget(controller.player.gridPos, self.xTar, self.yTar)
                if (self.gridPos[0] - 4 <= self.targetGrid[0] <= self.gridPos[0] + 4) or (self.gridPos[1] - 4 <= self.targetGrid[1] <= self.gridPos[1] + 4):
                    self.targetGrid = self.scatterGrid
            
        # Second state - Ghosts enter this state at set intervals
        elif self.state == 'scatter':
            self.targetGrid = self.scatterGrid
            # Blinky heads to the NE corner
            # Pinky heads to the NW coner
            # Inky heads to the SE corner
            # Clyde heads to the SW corner

        elif self.state == 'flee':
            #
            #[-2,0,2,0] [0,-2,0,2]
            pass

        elif self.state == 'dead':
            self.targetGrid = [ self.spawnPos[0]//CELLWIDTH , self.spawnPos[1]//CELLHEIGHT ]
            if self.gridPos == self.targetGrid:
                self.state = 'chase'

        self.getNextMove(controller)
        self.moveDir(controller)

    def getNextMove(self, controller):
        self.distanceToGrid = []
        self.dist = 0
        self.moveOffset = [0,0]

        if self.nextDirection != 'O':
            return

        # Get list of available moves to make and store in self.gridList
        if self.currentDirection == 'N':
            #if (self.gridPos[0], self.gridPos[1] - 1) not in controller.indexedWalls:
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

        elif self.currentDirection == 'O':
            self.nextGrid = [self.gridPos[0], self.gridPos[1]]
            for x, y in zip((0, 1, 0, -1), (-1, 0, 1, 0)):
                    if not any(wall.gridPos == [self.nextGrid[0]+x,self.nextGrid[1]+y] for wall in controller.walls):
                        self.gridList.append([self.nextGrid[0]+x,self.nextGrid[1]+y])

        # Use self.gridList to determine which grid is closest to target grid
        for gridID in self.gridList:
            self.dist = hypot( (self.targetGrid[0] - gridID[0]), (self.targetGrid[1] - gridID[1]) )
            self.distanceToGrid.append(self.dist)

        if len(self.distanceToGrid) > 0:
            self.moveOffset = self.distanceToGrid.index(min(self.distanceToGrid))
        else:
            self.gridList = [[0,0]]
            self.moveOffset = 0

        if self.nextGrid[0] == self.gridList[self.moveOffset][0] and self.nextGrid[1]-1 == self.gridList[self.moveOffset][1]:
            # X, Y-1 == N
            self.nextDirection = 'N'

        elif self.nextGrid[0]+1 == self.gridList[self.moveOffset][0] and self.nextGrid[1] == self.gridList[self.moveOffset][1]:
            # X+1, Y == E
            self.nextDirection = 'E'

        elif self.nextGrid[0] == self.gridList[self.moveOffset][0] and self.nextGrid[1]+1 == self.gridList[self.moveOffset][1]:
            # X, Y+1 == S
            self.nextDirection = 'S'
        
        elif self.nextGrid[0]-1 == self.gridList[self.moveOffset][0] and self.nextGrid[1] == self.gridList[self.moveOffset][1]:
            # X-1, Y == W
            self.nextDirection = 'W'
        
        else:
            self.currentDirection = 'O'

        if not DEBUG:   # if not in debug mode, clean out list here instead of after they're drawn
            self.gridList = []
