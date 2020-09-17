class GameField:
    lives = ""          # Amount of lives Pac-Man has left
    score = 0           # The score of the current game
    level = "1-1"       # The current level
    time = 0            # Time elapsed while in game
    difficulty = 1.0    # The current difficulty of the game

    def __init__(self, lives, score, level, time, difficulty):
        self.lives = lives
        self.score = score
        self.level = level
        self.time = time
        self.difficulty = difficulty

class Interactable:
    interactableType = ""    # Valid types are: dot, fruit, powerpellet, ghost
    
    def __init__(self,interactableType):
        self.interactableType = interactableType

    def collision():
        if self.interactableType == "dot":
            self.remove()
            return (10)
        elif self.interactableType == "fruit":
            self.remove()
            return (50)
        elif self.interactableType == "powerpellet":
            self.remove()
            return ("stateswap")
        elif self.interactableType == "ghost":
            return ("dedm8")
        else:
            return ("error")
    
    def remove():
        del self

class Movement:
    currentDirection = ""   # The current direction of the object
    nextDirection = ""      # The next planned direction of the object
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

class PacMan(Movement):
    state = ""          # Valid states are: inactive, active, powerup, dead
    
    def __init__(self, state):
        self.state = state

class Ghost(Interactable, Movement):
    personality = ""    # Valid personalities are: Inky, Blinky, Pinky, Clyde
    state = ""          # Valid States are: inactive, active, flee, dead, alternate

    def __init__(self, personality, state):
        super().__init__():
        self.personality = personality
        self.state = state

pinky = Ghost("ghost", "W", "N", 1.0, 35, 934, "Pinky", "inactive")
print(pinky)

