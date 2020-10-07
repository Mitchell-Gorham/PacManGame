import pygame
import sys
import random
from settings import *

from pacmanClass import PacMan

pygame.init()



class GameClass:
    def __init__(self): #, lives, score, level, time, difficulty, state, player, interactables, ghosts, dots):
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        self.lives = 3          # Amount of lives Pac-Man has left
        self.score = 0          # The score of the current game
        self.level = 1          # The current level
        self.time = 0           # Time elapsed while in game
        self.difficulty = 1.0   # The current difficulty of the game
        self.running = True     # Core Game Loop Active
        self.state = 'init'     # Current game state, viable ones: init, inactive, active, gameover
        
        self.statePrev = ''     # Debug
        self.nextDir = ''       # Debug

        self.player = PacMan(self, self.state)  # The Player

        self.interactables = [] # All interactables, including ghosts and dots
        self.ghosts = []        # Array of the Ghosts
        self.dots = []          # Array of the Dots

        pygame.display.set_caption('PacMan')
        self.run()

    ### Initialisation ###
    def initDrawEvents(self):
                
        self.screen.fill(BLACK)
        self.drawText(self.screen, 'SPACEBAR TO START', (WIDTH/2,HEIGHT/2), 'arial black', 16, WHITE)

        pygame.display.update()

    def initKeyEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                #First run init events
                self.state = 'active'

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

            # Debug
            if DEBUG and self.statePrev != self.state:
                print('Now running in: '+ self.state)
                self.statePrev = self.state

            if self.state == 'init':
                self.initKeyEvents()
                self.initDrawEvents()
            elif self.state == 'active':
                self.loopKeyEvents()
                self.updateMovement()
                self.loopDrawEvents()
                #activeDraw()
            elif self.state == 'gameover':
                pass
                #gameoverEvents()
                #save the score or something
                #Go back to the init phase
            else:
                self.running = False
            pygame.time.Clock().tick(FPS)
        pygame.quit()
        sys.exit()

    def loopDrawEvents(self):
        # Maze
        self.screen.fill(BLACK)
        self.background = pygame.Surface((WIDTH-20,HEIGHT-HEIGHTBUFFER-10))
        self.background.fill(BLUE)
        self.screen.blit(self.background, (10,HEIGHTBUFFER/2))

        #Player 
        self.player.draw()

        #Ghosts


        #Interactables


        pygame.display.update()

    def loopKeyEvents(self):
        ### Player Key Detection for Movement ###
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    self.player.nextDirection = "N"
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.player.nextDirection = "E"
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.player.nextDirection = "S"
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.player.nextDirection = "W"
            
            # Debug
            if DEBUG and self.nextDir != self.player.nextDirection:
                print('Moving: '+ self.player.nextDirection)
                self.nextDir = self.player.nextDirection
            


    ### Update Movement for Players and Ghosts ###
    def updateMovement(self):
        # Update the player's position
        # First check to see if the player's next direction is valid
        # if it is, set their current direction to the next direction, set next direction to O (null)
        
        self.player.moveDir()
      

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
        else:
            if self.difficulty > 1.1:
                self.difficulty -= 0.2  # Slightly lower the difficulty on death
            self.lifeRestartEvent()
        
    
    ### Reset player and enemy positions and start game delay again ###
    def lifeRestartEvent(self):
        pass


    ### Game Over Functions ###


    ### Other Fuctions ###

    def drawText(self, screen, text, position, fontStyle, size, colour):
        font = pygame.font.SysFont(fontStyle, size)
        text = font.render(text, False, colour)
        screen.blit(text, position)
