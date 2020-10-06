import pygame
import sys
import random
from settings import *

from pacmanClass import PacMan

#pygame.init()

class GameClass:
    def __init__(self): #, lives, score, level, time, difficulty, state, player, interactables, ghosts, dots):
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        self.lives = 3          # Amount of lives Pac-Man has left
        self.score = 0          # The score of the current game
        self.level = 1          # The current level
        self.time = 0           # Time elapsed while in game
        self.difficulty = 1.0   # The current difficulty of the game
        self.running = False
        self.state = 'init'   # Current game state, viable ones: init, inactive, active, gameover

        self.player = PacMan(self.state)  # The Player

        self.interactables = [] # All interactables, including ghosts and dots
        self.ghosts = []        # Array of the Ghosts
        self.dots = []          # Array of the Dots
        self.run()

    ### Initialisation ###
    def initEvents(self):
        pygame.display.set_caption('PacMan')
        
        self.screen.fill(BLACK)
        #Somehow self.drawText()

    def levelStartEvents(self):
        ### Moves objects to their starting positions - Does recreate non-ghost interactables
        pass

    ### Active ###
    def checkDotCount(self):
        ### Counts the amount of dots+powerups left, if it's 0, go to the next level
        pass

    ### GameOver ###
    def resetEvents(self):
        ### Clear everything out and re-initialise the game
        pass

    ### Game Loop Functions ###
    def run(self):
        while self.running:
            if self.state == 'init':
                self.initEvents()
            elif self.state == 'active':
                self.loopEvents()
                self.updateMovement()
                #activeDraw()
            elif self.state == 'gameover':
                pass
                #gameoverEvents()
            else:
                self.running = False
            pygame.time.Clock.tick(FPS)
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
            if self.player.position == interactable.location:
                # interactable.collision(self, self.player)
                if interactable.interactableType == 'd':
                    self.score += 10
                    interactable.remove()
                    self.checkDotCount()
                elif interactable.interactableType == 'f':
                    self.score += 50
                    interactable.remove()
                elif interactable.interactableType == 'p':
                    self.player.powerup()
                    interactable.remove()
                    self.checkDotCount()
                elif interactable.interactableType == 'g':
                    if self.player.state != 'powerup':
                        self.lifeLoss()
                    else:
                        interactable.state = 'dead'


    ### Life Loss ###
    def lifeLoss(self):
        self.lives -= 1 
        if self.lives == 0:       
            self.state = "gameover"
        if self.difficulty > 1.1:
            self.difficulty -= 0.2  # Slightly lower the difficulty on death
        self.lifeRestartEvent()
    
    ### Reset player and enemy positions and start game delay again ###
    def lifeRestartEvent(self):
        pass


    ### Game Over Functions ###


    ### Other Fuctions ###

    def drawText(self, screen, text, position, font, size, colour):
        font = pygame.font.SysFont(font, size)
        text = font.render(text, False, colour)
        screen.blit(text, position)
