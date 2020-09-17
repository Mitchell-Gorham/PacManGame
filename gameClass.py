import pygame
import sys
import random
from classes import *

#pygame.init()

class GameField:
    def __init__(self, lives, score, level, time, difficulty):
        self.lives = 3          # Amount of lives Pac-Man has left
        self.score = 0          # The score of the current game
        self.level = 1          # The current level
        self.time = 0           # Time elapsed while in game
        self.difficulty = 1.0   # The current difficulty of the game

        self.player = PacMan("inactive")

### Initialisation Functions ###

    def init_events(self):
        self.lives = 3

### Game Loop Functions ###

    def loop_events(self):

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

    def update_movement(self):
        # Update the player's position

        # Update the enemies positions

            


### Game Over Functions ###