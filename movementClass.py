# N = [0, -1] 
# E = [1, 0] 
# S = [0, 1] 
# W = [-1, 0]
import os
from settings import CELLWIDTH, CELLHEIGHT, WIDTH

class Movement:   
    def __init__(self):
        self.currentDirection = 'O'   # The current direction of the object: N, E, S ,W, O
        self.nextDirection = 'O'      # The next planned direction of the object: N, E, S , W, O
        self.speed = 2.0              # The speed of the object
        self.xPos = 0                 # The x position of the object
        self.yPos = 0                 # The y position of the object
        self.position = [self.xPos,self.yPos]   # The x and y positions of the object
        self.gridPos = []             # The grid position of the object on the game field
        self.spawnPos = [self.xPos,self.yPos]

    def moveDir(self, controller, state):   # Moves in the direction
        self.nextDirFree(controller, state)      # Check to see if you can change direction
        self.currentDirFree(controller, state)   # Then, check to see if you can move in your current direction

        if self.currentDirection == 'N':
            self.position = [int(self.xPos+(0 * self.speed)),
                                int(self.yPos+(-1 * self.speed))]
        elif self.currentDirection == 'E':
            self.position = [int(self.xPos+(1 * self.speed)),
                                int(self.yPos+(0 * self.speed))]
        elif self.currentDirection == 'S':
            self.position = [int(self.xPos+(0 * self.speed)),
                                int(self.yPos+(1 * self.speed))] 
        elif self.currentDirection == 'W':
            self.position = [int(self.xPos+(-1 * self.speed)),
                                int(self.yPos+(0 * self.speed))]

        # Reflect these changes in positon to your x and y coords
        self.checkTele()
        self.updatePos()

    def nextDirFree(self, controller, state):  # Are you able to go in your desired nextDirection
        canMove = True
        nextLocations = {
            'N': [self.gridPos[0], self.gridPos[1] - 1],
            'E': [self.gridPos[0] + 1, self.gridPos[1]],
            'S': [self.gridPos[0], self.gridPos[1] + 1],
            'W': [self.gridPos[0] - 1, self.gridPos[1]]
        }

        if self.nextDirection not in nextLocations:
            return

        nextPosition = nextLocations[self.nextDirection]

        for wall in controller.walls:
            if state in ('activated','dead'):
                if wall.wallType in ('w', 'i'):
                    if wall.gridPos == nextPosition:
                        canMove = False
                        break
            elif wall.gridPos == nextPosition:
                canMove = False
                break
        if canMove:
            self.currentDirection = self.nextDirection
            self.nextDirection = 'O'

        return

    def currentDirFree(self, controller, state):  # Are you able to go in your desired currentDirection
        if state not in ('activated','dead'):
            if self.currentDirection == 'N':
                for wall in controller.walls:
                    if wall.gridPos == [self.gridPos[0], self.gridPos[1]-1]:
                        self.currentDirection = 'O'
                        break

            elif self.currentDirection == 'E':
                for wall in controller.walls:
                    if wall.gridPos == [self.gridPos[0]+1, self.gridPos[1]]:
                        self.currentDirection = 'O'
                        break                   

            elif self.currentDirection == 'S':
                for wall in controller.walls:
                    if wall.gridPos == [self.gridPos[0], self.gridPos[1]+1]:
                        self.currentDirection = 'O'
                        break
            
            elif self.currentDirection == 'W':
                for wall in controller.walls:
                    if wall.gridPos == [self.gridPos[0]-1, self.gridPos[1]]:
                        self.currentDirection = 'O'
                        break

    def checkTele(self):
        if self.gridPos == [28,17] and self.currentDirection == 'E': # and self.currentDirection != 'W':
            self.position = [-10, 340]
        elif self.gridPos == [28,17] and self.currentDirection != 'W':
            self.currentDirection = 'E'
            self.checkTele()
        if self.gridPos == [-1,17] and self.currentDirection == 'W': # and self.currentDirection != 'E':
            self.position = [WIDTH+10, 340]
        elif self.gridPos == [-1,17] and self.currentDirection != 'E':
            self.currentDirection = 'W'
            self.checkTele()

    def updatePos(self):
        self.xPos = self.position[0]
        self.yPos = self.position[1]
        self.gridPos = [ self.xPos//CELLWIDTH , self.yPos//CELLHEIGHT ]    
