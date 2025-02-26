import pygame as p

WIDTH = HEIGHT = 512
DIMENSION = 8
SCALER = 100

SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}
DOTS = {}

PADDING = 30

BACKGROUND_COLOR = p.Color("white")

BOARD_SQUARE_COLOUR = p.Color("beige")
BOARD_SQUARE_COLOUR_2 = p.Color("pale green4")
SQUARE_SELECTED_COLOUR = p.Color("slate gray3")
SQUARE_VALID_MOVE_COLOUR = p.Color("honeydew2")

# Colours for future choices
# palegreen4
# turquoise4