# N = [0, -1] 
# E = [1, 0] 
# S = [0, 1] 
# W = [-1, 0]

from settings import *

class Movement:
    currentDirection = 'O'   # The current direction of the object: N, E, S ,W, O
    nextDirection = 'O'      # The next planned direction of the object: N, E, S ,W, O
    speed = 5.0             # The speed of the object
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

    def moveDir(self):  # Moves in the direction
        self.nextDirFree()

        if self.nextDirection == 'N':
            self.position = [int(self.xPos+(0 * self.speed)),
                             int(self.yPos+(-1 * self.speed))]
        elif self.nextDirection == 'E':
            self.position = [int(self.xPos+(1 * self.speed)),
                             int(self.yPos+(0 * self.speed))]
        elif self.nextDirection == 'S':
            self.position = [int(self.xPos+(0 * self.speed)),
                             int(self.yPos+(1 * self.speed))] 
        elif self.nextDirection == 'W':
            self.position = [int(self.xPos+(-1 * self.speed)),
                             int(self.yPos+(0 * self.speed))]
        else:
            pass

        self.updatePos()

    def nextDirFree(self):  # Are you able to go in your desired nextDirection
        if self.nextDirection == 'N':
            if self.yPos-10 <= HEIGHTBUFFER/2 + self.speed:   #Replace Pos?10 with Cell/Sprite Size
                self.currentDirection = 'O'
                self.nextDirection = 'O'

        if self.nextDirection == 'E':
            if self.xPos+10 >= WIDTH-10 - self.speed:   #Replace Pos?10 with Cell/Sprite Size
                self.currentDirection = 'O'
                self.nextDirection = 'O'

        if self.nextDirection == 'S':
            if self.yPos+10 >= (HEIGHT-(HEIGHTBUFFER/2)) - self.speed:   #Replace Pos?10 with Cell/Sprite Size
                self.currentDirection = 'O'
                self.nextDirection = 'O'

        if self.nextDirection == 'W':
            if self.xPos-10 <= 10 + self.speed:   #Replace Pos?10 with Cell/Sprite Size
                self.currentDirection = 'O'
                self.nextDirection = 'O'

    def updatePos(self):
        self.xPos = self.position[0]
        self.yPos = self.position[1]
