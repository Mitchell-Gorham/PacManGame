# N = [0, -1] 
# E = [1, 0] 
# S = [0, 1] 
# W = [-1, 0]

class Movement:
    currentDirection = ''   # The current direction of the object: N, E, S ,W, O
    nextDirection = ''      # The next planned direction of the object: N, E, S ,W, O
    speed = 1.0             # The speed of the object
    xPos = 0.0              # The x position of the object
    yPos = 0.0              # The y position of the object
    position = [xPos,yPos]  # The x and y positions of the object

    def __init__(self, currentDirection, nextDirection, speed,xPos,yPos):
        self.currentDirection = currentDirection
        self.nextDirection = nextDirection
        self.speed = speed
        self.xPos = xPos
        self.yPos = yPos
        self.position = [xPos,yPos]

    def nextDirFree(self):  # Are you able to go in your desired nextDirection
        if self.nextDirection == 'N':
            if self.position + [0,-1]:
                pass

    def moveDir(self):  # Moves in the direction
        self.position += self.currentDir*speed