import sys
from math import floor
import random

from settings import *
from pacmanClass import PacMan
from ghostClass import Ghost
from interactableClass import Interactable

import pygame

pygame.init()

class GameClass:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        self.lives = 3          # Amount of lives Pac-Man has left
        self.score = 0          # The score of the current game
        self.hiScore = 180    # The previous highscore = Loaded from file
        self.bonuses = [ORANGE, ORANGE, ORANGE, CYAN, ORANGE, RED, PINK]       # Bonus fruit collected
        self.lifeBonus = BONUSLIFE # Points needed for bonus life
        self.level = 1          # The current level
        self.time = 0           # Time elapsed while in game
        self.difficulty = 1.0   # The current difficulty of the game

        self.running = True     # Core Game Loop Active
        self.state = 'init'     # Current game state, viable ones: init, inactive, active, gameover

        self.player = PacMan(self, 'active')  # The Player

        self.interactables = [] # Contains dots, power pellets and bonus fruits
        self.ghosts = []        # Array of the Ghosts
        
        self.statePrev = ''     # Debug
        self.nextDir = ''       # Debug

        pygame.display.set_caption('PacMan')
        
        self.run()

    ### Initialisation ###
   
    def initDrawEvents(self):             
        self.screen.fill(BLACK)
        self.drawText(self.screen,'SPACEBAR TO START',
                     [WIDTH/2, HEIGHT/2], 'arial black',                        
                     16, WHITE, centered=True)

        pygame.display.update()

    def initKeyEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                #First run init events
                self.state = 'active'
                self.levelStartEvents()

    def levelStartEvents(self):
        ### Moves objects to their starting positions

        # PacMan Start Location
        self.player.position = [280,530]
        self.player.updatePos()
        
        # Ghost Start Location
        for i in range(4):
            self.ghosts.append(Ghost(self, i, 'inactive'))

        self.ghosts[0].position = [280,290]
        self.ghosts[0].updatePos()

        for i in range(1, len(self.ghosts)):
            self.ghosts[i].position = [240+((i-1)*40),350]
            self.ghosts[i].updatePos()
        
        for i in range(20):
            self.interactables.append(Interactable(self, 
                                        [20+CELLWIDTH*i+CELLWIDTH//2,
                                        CELLHEIGHT*10+CELLHEIGHT//2],
                                        0))

        self.updateStaticDraw()

    ### Active ###
    def checkDotCount(self):
        ### Counts the amount of dots+powerups left, if it's 0, go to the next level
        if len(self.interactables) <= 0:
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
                self.initDrawEvents()
                self.initKeyEvents()
            elif self.state == 'active':
                self.loopKeyEvents()
                self.updateMovement()
                self.loopDrawEvents()

                self.time = self.time+1
                if (self.time/10)%50 == 0:
                    self.difficulty = round(self.difficulty + 0.1,2)
                    self.updateStaticDraw()

            elif self.state == 'gameover':
                self.state == 'init'
                #gameoverEvents()
                #save the score or something
                #Go back to the init phase
            else:
                self.running = False
            pygame.time.Clock().tick(FPS)
        pygame.quit()
        sys.exit()

    def loopDrawEvents(self):
        # Background
        self.background = pygame.Surface((GAMEWIDTH,GAMEHEIGHT))
        self.background.fill([40,40,40])
        self.screen.blit(self.background, (0,HEIGHTBUFFER))

        # Interactables (Dots/Fruit/Etc)
        for i in range(len(self.interactables)):
            self.interactables[i].drawI()

        # Ghosts
        for i in range(len(self.ghosts)):
            self.ghosts[i].draw()

        # Player 
        self.player.draw()

        if DEBUG:
            self.drawText(self.screen, 
                            (str(self.player.gridPos[0])+","+str(self.player.gridPos[1])),
                            [self.player.xPos+15,self.player.yPos-15],
                            'arial black',10,WHITE,centered=True)

        # Debug grid
        if DEBUG:
            for x in range(WIDTH//CELLWIDTH):
                pygame.draw.line(self.screen,[70,70,70], (x*CELLWIDTH, 0), (x*CELLWIDTH, HEIGHT))
            for y in range(HEIGHT//CELLHEIGHT):
                pygame.draw.line(self.screen,[70,70,70], (0, y*CELLHEIGHT), (WIDTH, y*CELLHEIGHT))


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
                if DEBUG and event.key == pygame.K_ESCAPE:
                    self.running = False
            
    def updateStaticDraw(self):
        # Top Black Band
        self.topStaticBackground = pygame.Surface((GAMEWIDTH,HEIGHTBUFFER))
        self.topStaticBackground.fill(BLACK)
        self.screen.blit(self.topStaticBackground, (0,0))
        # Bot Black Band
        self.botStaticBackground = pygame.Surface((GAMEWIDTH,HEIGHTBUFFER))
        self.botStaticBackground.fill(BLACK)
        self.screen.blit(self.botStaticBackground, (0,HEIGHTBUFFER+GAMEHEIGHT))
        # Text
        self.drawText(self.screen, 'SCORE', [20,17], 'arial black', 16, WHITE)
        self.drawText(self.screen, str(self.score), [20,38], 'arial black', 16, WHITE)      
        
        self.drawText(self.screen, 'HI-SCORE', [int(WIDTH/2)-40,17], 'arial black', 16, WHITE)
        self.drawText(self.screen, str(self.hiScore), [int(WIDTH/2)-25,38], 'arial black', 16, WHITE)

        for i in range(self.lives):
            pygame.draw.circle(self.screen, YELLOW, (20+(25*i), int(HEIGHT-HEIGHTBUFFER+15)),PLAYERRADIUS)
        for i in range(len(self.bonuses)):
            pygame.draw.circle (self.screen, self.bonuses[i], (WIDTH-20-(25*i), int(HEIGHT-HEIGHTBUFFER+15)),PLAYERRADIUS)
        

        # Debug
        if DEBUG:
            self.drawText(self.screen, 'time: {}'.format(floor(self.time/10)), [(WIDTH-60),16], 'arial black', 10, WHITE)
            self.drawText(self.screen, 'diff: {}'.format(self.difficulty), [(WIDTH-60),26], 'arial black', 10, WHITE)

        pygame.display.update()

    ### Update Movement for Players and Ghosts ###
    def updateMovement(self):
        # Update the player's position     
        self.player.moveDir()
        
        for i in range(len(self.ghosts)):
            self.ghosts[i].moveDir()
            if self.time%50 == 0:
                x = random.choice(["N","N","N", "E","E","E", "S","S","S", "W","W","W"])
                self.ghosts[i].currentDirection = x
                #print(str(i)+" is given dir: "+str(x))

        # Check to see if player shares a grid with an interactable
        for interactable in self.interactables:
            if interactable.gridPos == self.player.gridPos:
                if interactable.interactableType >= 2:
                    self.bonuses.append(interactable)
                elif interactable.interactableType == 1:
                    for i in range(len(self.ghosts)):
                        self.ghosts[i].setFlee()
                
                self.updateScore(interactable.score)              
                interactable.remove(self.interactables, self.interactables.index(interactable))
                self.updateStaticDraw()
                self.checkDotCount()
        
        # Or shares it with a ghost!
        for ghost in self.ghosts:
            if ghost.gridPos == self.player.gridPos:
                if ghost.state != 'flee':
                    #self.lifeLoss()
                    pass
                else:
                    ghost.state = 'dead'
        
    ### Life Loss ###
    def lifeLoss(self):
        self.lives -= 1
        self.updateStaticDraw()
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

    def updateScore(self, scoreValue):
        self.score += scoreValue
        if BONUSLIFE != 0:
            self.lifeBonus -= scoreValue    # Points deducted from amount needed for bonus life
            if self.lifeBonus <= 0:
                self.lives += 1
                self.lifeBonus = BONUSLIFE + self.lifeBonus
        if self.score > self.hiScore:
            self.hiScore = self.score


    def drawText(self, screen, text, position, fontStyle, size, colour, centered=False):
        font = pygame.font.SysFont(fontStyle, size)
        text = font.render(text, False, colour)
        
        text_size = text.get_size()
        if centered:
            position[0] = position[0]-text_size[0]//2
            position[1] = position[1]-text_size[1]//2
        
        screen.blit(text, position)
