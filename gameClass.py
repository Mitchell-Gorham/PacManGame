import sys
from math import floor
import random

from settings import *
from pacmanClass import PacMan
from ghostClass import Ghost
from interactableClass import Interactable
from wallClass import Wall

import pygame

pygame.init()

class GameClass:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        self.lives = 2          # Amount of lives Pac-Man has left
        self.score = 0          # The score of the current game
        self.hiScore = 25000    # The previous highscore = Loaded from file
        self.ghostBonusMulti = 1
        self.bonuses = [ORANGE, ORANGE, ORANGE, CYAN, ORANGE, RED, PINK] # Bonus fruit collected
        self.lifeBonus = BONUSLIFE # Points needed for bonus life
        self.level = 1          # The current level
        self.time = 0           # Time elapsed while in game
        self.difficulty = 1.0   # The current difficulty of the game

        self.running = True     # Core Game Loop Active
        self.state = 'init'     # Current game state, viable ones: init, inactive, active, gameover

        self.player = PacMan(self, 'active')  # The Player
        self.ghosts = []        # Array of the Ghosts
        for i in range(4):
            self.ghosts.append(Ghost(self, i, 'chase'))

        self.walls = []         # Contains the location of walls
        self.interactables = [] # Contains dots and power pellets
        
        
        self.statePrev = ''     # Debug
        self.nextDir = ''       # Debug

        pygame.display.set_caption('PacMan')
        
        self.run()

    ### Event-Driven Loop ###

    def run(self):
        while self.running:

            # Debug
            if DEBUG and self.statePrev != self.state:
                print('Now running in: '+ self.state)
                self.statePrev = self.state

            if self.state == 'init':
                self.initDrawEvents()
                self.initKeyEvents()
            elif self.state == 'loop':
                self.loopKeyEvents()
                self.updateMovement()
                self.loopDrawEvents()

                self.time = self.time+1
                if (self.time/10)%50 == 0:
                    self.difficulty = round(self.difficulty + 0.1,2)
                    self.updateStaticDraw()
                #if self.time%500 == 0:
                #    print('Swapping State')
                #    for ghost in self.ghosts:
                #        if ghost.state == 'chase':
                #            ghost.state = 'scatter'
                #        elif ghost.state == 'scatter':
                #            ghost.state = 'chase'

            elif self.state == 'gameover':
                self.goDrawEvents()
                self.goKeyEvents()

            else:
                self.running = False
            pygame.time.Clock().tick(FPS)
        pygame.quit()
        sys.exit()

    ### Initialisation ###
   
    def initDrawEvents(self):   # Draws initial Title Screen and the Current Level

        self.screen.fill(BLACK)
        self.drawText(self.screen,'SPACEBAR TO START',
                     [WIDTH/2, HEIGHT/2], 'arial black',                        
                     16, WHITE, centered=True)
        self.drawText(self.screen,'LEVEL: '+str(self.level),
                     [WIDTH/2, HEIGHT/2+20], 'arial black',                        
                     16, WHITE, centered=True)

        pygame.display.update()

    def initKeyEvents(self):    # Listens for the spacebar Event to proceed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                #First run init events
                self.state = 'loop'
                self.initLevelStart()

    def initLevelStart(self): # Sets up the level based on a fed .txt file
        # Cleans out  level arrays
        self.walls = []
        self.interactables = []

        ### Moves objects to their starting positions
        self.resetPlayerGhostPositions()

        #Load Layout from File
        with open("walls.txt", 'r') as file:
            for yidx, line in enumerate(file):
                for xidx, char in enumerate(line):
                    if char in ('w', '_', 'i'):
                        self.walls.append(Wall(self,
                            [CELLWIDTH*xidx, CELLHEIGHT*yidx+HEIGHTBUFFER], char
                            ))
                    elif char == '0':
                        self.interactables.append(Interactable(self,
                            [CELLWIDTH*xidx+CELLWIDTH//2,
                            CELLHEIGHT*yidx+CELLHEIGHT//2+HEIGHTBUFFER],
                            int(char)
                            ))
                    elif char == '1':
                        self.interactables.append(Interactable(self,
                            [CELLWIDTH*xidx+CELLWIDTH//2,
                            CELLHEIGHT*yidx+CELLHEIGHT//2+HEIGHTBUFFER],
                            int(char)
                            ))

        self.updateStaticDraw()

    ### Game Loop Functions ###

    def loopKeyEvents(self):
        ### Player Key Detection for Movement ###
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    self.player.nextDirection = 'N'
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.player.nextDirection = 'E'
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.player.nextDirection = 'S'
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.player.nextDirection = 'W'
            # Debug    
                if DEBUG and event.key == pygame.K_ESCAPE:
                    self.running = False
            
    def updateMovement(self):
        # Update the player's position 
        if DEBUG and self.nextDir != self.player.nextDirection:
            #print('Next Move: '+ self.player.nextDirection)
            self.nextDir = self.player.nextDirection    
        
        self.player.moveDir(self, 'active')
        for ghost in self.ghosts:
            ghost.personalityFunc()
            
        
        # Check to see if player shares a grid with an interactable
        for interactable in self.interactables:
            if interactable.gridPos == self.player.gridPos:
                if interactable.interactableType >= 2:
                    self.bonuses.append(interactable)
                elif interactable.interactableType == 1:
                    self.ghostBonusMulti = 1
                    for i in range(len(self.ghosts)):
                        self.ghosts[i].setFlee()
                
                self.updateScore(interactable.score)              
                interactable.remove(self.interactables, self.interactables.index(interactable))
                self.checkDotCount()
        
        # Or shares it with a ghost!
        for ghost in self.ghosts:
            if ghost.gridPos == self.player.gridPos:
                if ghost.state in ('chase', 'scatter'):
                    self.lifeLoss()
                elif ghost.state == 'flee':
                    self.updateScore((200*self.ghostBonusMulti))
                    self.ghostBonusMulti *= 2
                    ghost.state = 'dead'

    def loopDrawEvents(self):
        # Background
        self.background = pygame.Surface((GAMEWIDTH,GAMEHEIGHT))
        self.background.fill(BLACK)
        self.screen.blit(self.background, (0,HEIGHTBUFFER))

        # Walls
        for i in range(len(self.walls)):
            self.walls[i].draw()

        # Interactables (Dots/Fruit/Etc)
        for i in range(len(self.interactables)):
            self.interactables[i].draw()

        # Ghosts
        for i in range(len(self.ghosts)):
            self.ghosts[i].draw()

        # Player 
        self.player.draw()

        # DEBUG
        if DEBUG:
            # Player Grid Loc
            self.drawText(self.screen, 
                            (str(self.player.gridPos[0])+","+str(self.player.gridPos[1])),
                            [self.player.xPos+15,self.player.yPos-15],
                            'arial black',10,WHITE,centered=True)

            # Debug grid
            for x in range(GAMEWIDTH//CELLWIDTH):
                pygame.draw.line(self.screen,[70,70,70], (x*CELLWIDTH, HEIGHTBUFFER), (x*CELLWIDTH, GAMEHEIGHT+HEIGHTBUFFER))
            for y in range(GAMEHEIGHT//CELLHEIGHT):
                pygame.draw.line(self.screen,[70,70,70], (0, y*CELLHEIGHT+HEIGHTBUFFER), (WIDTH, y*CELLHEIGHT+HEIGHTBUFFER))
            
            # Movement/Target Grid
            self.pacRect = pygame.Rect(self.player.gridPos[0]*CELLWIDTH,self.player.gridPos[1]*CELLHEIGHT,CELLWIDTH,CELLHEIGHT)
            pygame.draw.rect(self.screen, [0,255,0], self.pacRect,1)

            for ghost in self.ghosts:
                self.ghostRect = pygame.Rect(ghost.gridPos[0]*CELLWIDTH, ghost.gridPos[1]*CELLHEIGHT,CELLWIDTH,CELLHEIGHT)
                pygame.draw.rect(self.screen, ghost.colour[ghost.personality], self.ghostRect,1)
                self.ghostRect = pygame.Rect(ghost.targetGrid[0]*CELLWIDTH, ghost.targetGrid[1]*CELLHEIGHT,CELLWIDTH,CELLHEIGHT)
                pygame.draw.rect(self.screen, ghost.colour[ghost.personality], self.ghostRect,1)
                self.ghostRect = pygame.Rect(ghost.nextGrid[0]*CELLWIDTH, ghost.nextGrid[1]*CELLHEIGHT,CELLWIDTH,CELLHEIGHT)
                pygame.draw.rect(self.screen, ghost.colour[ghost.personality], self.ghostRect,1)
                #print({ 'gridList': ghost.gridList, 'dist': ghost.distanceToGrid })
                for idx, i in enumerate(ghost.gridList):
                    self.ghostRect = pygame.Rect(i[0]*CELLWIDTH, i[1]*CELLHEIGHT,CELLWIDTH,CELLHEIGHT)
                    pygame.draw.rect(self.screen, ghost.colour[ghost.personality], self.ghostRect,1)

                    self.drawText(self.screen, ghost.nextDirection, [ghost.xPos-15, ghost.yPos-15], 'arial black', 8, WHITE)

                    #self.drawText(self.screen, str(round(ghost.distanceToGrid[idx], 1)), [self.ghostRect[0], self.ghostRect[1]], 'arial black', 8, WHITE)

                if i == 2:
                    self.drawText(self.screen, str(ghost.xTar, ghost.yTar), [ghost.xPos-25, ghost.yPos], 'arial black', 8, WHITE)
                
                pygame.draw.line(self.screen,
                                ghost.colour[ghost.personality],
                                (ghost.xPos, ghost.yPos),
                                (ghost.targetGrid[0]*CELLWIDTH+10, ghost.targetGrid[1]*CELLHEIGHT+10),
                                1)

                ghost.gridList = []

        pygame.display.update()  
    
    ### Game Over Functions ###
   
    def goDrawEvents(self):   # Draws Game Over Screen

        self.screen.fill(BLACK)
        self.drawText(self.screen,'GAME OVER',
                     [WIDTH/2, HEIGHT/2-HEIGHTBUFFER], 'arial black',                        
                     16, RED, centered=True)
        self.drawText(self.screen,'SPACEBAR TO RESTART',
                     [WIDTH/2, HEIGHT/2], 'arial black',                        
                     16, WHITE, centered=True)
        self.drawText(self.screen,'SCORE: ',
                     [WIDTH/2-(WIDTH/6), HEIGHT/2+40], 'arial black',                        
                     16, WHITE, centered=True)
        self.drawText(self.screen,str(self.score),
                     [WIDTH/2-(WIDTH/6), HEIGHT/2+60], 'arial black',                        
                     16, WHITE, centered=True)
        self.drawText(self.screen,'HI-SCORE: ',
                     [WIDTH/2+(WIDTH/6), HEIGHT/2+40], 'arial black',                        
                     16, WHITE, centered=True)
        self.drawText(self.screen,str(self.hiScore),
                     [WIDTH/2+(WIDTH/6), HEIGHT/2+60], 'arial black',                        
                     16, WHITE, centered=True)

        if self.score == self.hiScore:
            self.drawText(self.screen,'NEW HI-SCORE',
                     [WIDTH/2, HEIGHT/2+HEIGHTBUFFER+20], 'arial black',                        
                     16, YELLOW, centered=True)

        pygame.display.update()

    def goKeyEvents(self):    # Listens for the spacebar Event to proceed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                #First run init events
                self.resetGame()

    ### Other Fuctions ###

    def drawText(self, screen, text, position, fontStyle, size, colour, centered=False):
        font = pygame.font.SysFont(fontStyle, size)
        text = font.render(text, False, colour)
        
        text_size = text.get_size()
        if centered:
            position[0] = position[0]-text_size[0]//2
            position[1] = position[1]-text_size[1]//2
        
        screen.blit(text, position)

    def updateScore(self, scoreValue):
        self.score += scoreValue
        if BONUSLIFE != 0:
            self.lifeBonus -= scoreValue    # Points deducted from amount needed for bonus life
            if self.lifeBonus <= 0:
                self.lives += 1
                self.lifeBonus = BONUSLIFE + self.lifeBonus
        if self.score > self.hiScore:
            self.hiScore = self.score

        self.updateStaticDraw()

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
        
        # Lives and Fruit
        for i in range(self.lives):
            pygame.draw.circle(self.screen, YELLOW, (20+(25*i), int(HEIGHT-HEIGHTBUFFER+15)),PLAYERRADIUS)
        for i in range(len(self.bonuses)):
            pygame.draw.circle (self.screen, self.bonuses[i], (WIDTH-20-(25*i), int(HEIGHT-HEIGHTBUFFER+15)),PLAYERRADIUS)

        # Debug
        if DEBUG:
            self.drawText(self.screen, 'time: {}'.format(floor(self.time/10)), [(WIDTH-60),16], 'arial black', 10, WHITE)
            self.drawText(self.screen, 'diff: {}'.format(self.difficulty), [(WIDTH-60),26], 'arial black', 10, WHITE)

        pygame.display.update()

    def checkDotCount(self):
        ### Counts the amount of dots+powerups left, if it's 0, go to the next level
        if len(self.interactables) <= 0:
            self.level += 1
            self.state = 'init'

    def lifeLoss(self):
        self.lives -= 1
        self.updateStaticDraw()
        if self.lives < 0:       
            self.state = 'gameover'
        else:
            if self.difficulty > 1.1:
                self.difficulty -= 0.2  # Slightly lower the difficulty on death
        
        self.resetPlayerGhostPositions()

    def resetPlayerGhostPositions(self):
        self.player.position = [280,530]
        self.player.updatePos()
        self.player.currentDirection = 'O'
        self.player.nextDirection = 'O'

        for ghost in self.ghosts:
            if ghost.personality == 0:
                ghost.state = 'chase'
                ghost.position = [280,290]
                ghost.spawnPos = ghost.position
                ghost.updatePos()
                ghost.currentDirection = 'O'
                ghost.nextDirection = 'O'        
            else:
                ghost.state = 'inactive'
                ghost.position = [240+((ghost.personality-1)*40),350]
                ghost.spawnPos = ghost.position
                ghost.updatePos()
                ghost.currentDirection = 'O'
                ghost.nextDirection = 'O'

    def resetGame(self):
        self.__init__()