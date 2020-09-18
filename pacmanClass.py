import movementClass

class PacMan(Movement):
    state = ""          # Valid states are: inactive, active, powerup, dead
    
    def __init__(self, state):
        self.state = state