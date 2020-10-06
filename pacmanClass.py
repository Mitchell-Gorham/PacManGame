from movementClass import *

class PacMan(Movement):
    state = ''         # Valid states are: inactive, active, powerup, dead
    
    def __init__(self, state):
        self.state = state

    def powerup(self, ):
        self.state = 'powerup'