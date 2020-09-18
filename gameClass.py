import pygame
import sys
import random

#pygame.init()

class GameField:
    def __init__(self, lives, score, level, time, difficulty, state, player, interactables, ghosts, dots):
        self.lives = 3          # Amount of lives Pac-Man has left
        self.score = 0          # The score of the current game
        self.level = 1          # The current level
        self.time = 0           # Time elapsed while in game
        self.difficulty = 1.0   # The current difficulty of the game
        self.state = 'inactive'   # Current game state, viable ones: inactive, active, gameover

        self.player = PacMan()  # The Player

        self.interactables = [] # All interactables, including ghosts and dots
        self.ghosts = []        # Array of the Ghosts
        self.dots = []          # Array of the Dots

    ### Initialisation ###
    def initEvents(self):
        self.lives = 3

    def levelStartEvents(self):
        ### Moves objects to their starting positions - Does recreate non-ghost interactables
        pass

    ### Active ###


    ### GameOver ###
    def resetEvents(self):
        pass

    ### Game Loop Functions ###
    def run(self):
        while.self.running:
            if self.state == 'inactive':
                pass
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
        # First check to see if the player's next direction is valid
        # if it is, set their current direction to the next direction, set next direction to O (null)
        if self.player.position: # [xPos,yPos] + [1,0]
            pass
        # Then, move the player
        if self.player.currentDirection:
            pass

        # Update the enemies positions
            # perform similar checks for each of the ghosts

        # Check to see if player is on top of an interactable
        for interactable in self.interactables:
            if self.player.location == interactable.location:
                interactable.collision(self, self.player)
                if interractable.interactableType == 'd':
                    self.score += 10
                    interactable.remove()
                    self.checkDotCount()
                elif interractable.interactableType == 'f':
                    self.score += 50
                    interactable.remove()
                elif interractable.interactableType == 'p':
                    self.player.powerup()
                    interactable.remove()
                    self.checkDotCount()
                elif interractable.interactableType == 'g':
                    if self.player.state != 'powerup':
                        self.lifeLost()
                    else interactable.state = 'dead'


    ### Life Loss ###
    def lifeLoss(self):
        self.lives -= 1 
        if self.lives == 0:       
            self.state = "gameover"
            break()
        if self.difficulty > 1.1:
            self.difficulty -= 0.2  # Slightly lower the difficulty on death
        self.lifeRestartEvent()
    
    ### Reset player and enemy positions and start game delay again ###
    def lifeRestartEvent():
        pass


    ### Game Over Functions ###