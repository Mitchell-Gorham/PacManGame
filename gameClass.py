import pygame
import sys
import random

#pygame.init()

class GameField:
    def __init__(self, lives, score, level, time, difficulty):
        self.lives = 3          # Amount of lives Pac-Man has left
        self.score = 0          # The score of the current game
        self.level = 1          # The current level
        self.time = 0           # Time elapsed while in game
        self.difficulty = 1.0   # The current difficulty of the game
        self.state = inactive   # Current game state, viable ones: inactive, active, gameover

        self.player = 

### State Functions ###

    ### Initialisation ###
    def initEvents(self):
        self.lives = 3

    ### Active ###


    ### GameOver ###
    # resetEvents(self):
    #

### Game Loop Functions ###
    def run(self):
        while.self.running:
            if self.state == 'inactive':
                
            elif state.start == 'active':
                loopEvents()
                updateMovement()
                #activeDraw()
            elif self.state == 'gameover':
                #gameoverEvents()
            else:
                self.running = False

            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()

    def loopEvents(self):

        ### Player Key Detection for Movement ###
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.type == pygame.K_UP or pygame.K_W:
                    self.player.nextDirection = "N"
                if event.type == pygame.K_RIGHT or pygame.K_D:
                    self.player.nextDirection = "E"
                if event.type == pygame.K_DOWN or pygame.K_S:
                    self.player.nextDirection = "S"
                if event.type == pygame.K_LEFT or pygame.K_A:
                    self.player.nextDirection = "W"

    ### Update Movement for Players and Ghosts ###
    def updateMovement(self):
        # Update the player's position

        # Update the enemies positions

        # Check to see if player is on top of an interactable


    ### Life Loss ###
    def lifeLoss(self):
        self.lives -= 1 
        if self.lives == 0:       
            self.state = "gameover"


### Game Over Functions ###