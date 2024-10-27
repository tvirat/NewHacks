import sys
import game
import pygame
from settings import WIDTH, HEIGHT, FPS, TITLE

# -----------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------- Global Variable Declaration -----------------------------------
# -----------------------------------------------------------------------------------------------------------------------------------

# List to hold coin positions
coins = []

# Player's score
score = 0

# Colors
button_bg = (2, 73, 91)
button_text = (241, 250, 251)

# List to hold obstacle positions
obstacles = []

# Player's lives
lives = 3

# High score
high_score = 0  # Initialize high score

game.start_screen()

