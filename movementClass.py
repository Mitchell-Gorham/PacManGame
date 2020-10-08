# N = [0, -1] 
# E = [1, 0] 
# S = [0, 1] 
# W = [-1, 0]

from settings import *

class Movement:
    currentDirection = 'O'   # The current direction of the object: N, E, S ,W, O
    nextDirection = 'O'      # The next planned direction of the object: N, E, S ,W, O
    speed = 2.0             # The speed of the object
    xPos = 0                # The x position of the object
    yPos = 0                # The y position of the object
    position = [xPos,yPos]  # The x and y positions of the object

    def __init__(self, currentDirection, nextDirection, speed,xPos,yPos):
        self.currentDirection = currentDirection
        self.nextDirection = nextDirection
        self.speed = speed
        self.xPos = xPos
        self.yPos = yPos
        self.position = [xPos,yPos]

    def moveDir(self):          # Moves in the direction
        self.nextDirFree()      # Check to see if you can change direction
        self.currentDirFree()   # Then, check to see if you can move in your current direction
        
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
        else:
            pass
        # Reflect these changes in positon to your x and y coords
        self.updatePos()

    def nextDirFree(self):  # Are you able to go in your desired nextDirection
        if self.nextDirection == 'N':
            if self.yPos - PLAYERRADIUS - self.speed <= HEIGHTBUFFER:
                pass
            else:
                self.currentDirection = self.nextDirection
                self.nextDirection = 'O'

        if self.nextDirection == 'E':
            if self.xPos + PLAYERRADIUS + self.speed >= WIDTH-10:
                pass
            else:
                self.currentDirection = self.nextDirection
                self.nextDirection = 'O'

        if self.nextDirection == 'S':
            if self.yPos + PLAYERRADIUS + self.speed >= HEIGHT-HEIGHTBUFFER:
                pass
            else:
                self.currentDirection = self.nextDirection
                self.nextDirection = 'O'

        if self.nextDirection == 'W':
            if self.xPos - PLAYERRADIUS - self.speed <= 10:
                pass
            else:
                self.currentDirection = self.nextDirection
                self.nextDirection = 'O'
    
    def currentDirFree(self):  # Are you able to go in your desired currentDirection
        if self.currentDirection == 'N':
            if self.yPos - PLAYERRADIUS - self.speed <= HEIGHTBUFFER:
                self.currentDirection = 'O'

        if self.currentDirection == 'E':
            if self.xPos + PLAYERRADIUS + self.speed >= WIDTH:
                self.currentDirection = 'O'

        if self.currentDirection == 'S':
            if self.yPos + PLAYERRADIUS + self.speed >= HEIGHT-HEIGHTBUFFER:
                self.currentDirection = 'O'
        
        if self.currentDirection == 'W':
            if self.xPos - PLAYERRADIUS - self.speed <= 0:
                self.currentDirection = 'O'

    def updatePos(self):
        self.xPos = self.position[0]
        self.yPos = self.position[1]
    
