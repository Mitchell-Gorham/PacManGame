class Movement:
    currentDirection = ""   # The current direction of the object: N, E, S ,W, O
    nextDirection = ""      # The next planned direction of the object: N, E, S ,W, O
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