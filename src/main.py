import pygame as p
from src import engine
from src.dimen.dimen import DIMENSION, IMAGES, WIDTH, HEIGHT, SQ_SIZE, COLOURS, MAX_FPS, WHITE_COLOUR, DARK_GRAY_COLOUR, \
    DARK_BLUE_COLOUR


def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(WHITE_COLOUR)
    game_state = engine.GameState()
    valid_moves = game_state.get_valid_moves()
    move_made = False # Flag variable for when a move is made

    load_images()
    running = True

    sq_selected = () #tuple i.e. (row, col)
    player_clicks = [] # two tuples - selecting piece to move (row, col), selecting where to move (row, col)
    
    while running:
        for event in p.event.get():
            if event.type == p.QUIT:
                running = False
            elif event.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE

                if sq_selected == (row, col):
                    sq_selected = ()
                    player_clicks = []
                else:
                    sq_selected = (row, col)
                    player_clicks.append(sq_selected)

                if len(player_clicks) == 2:
                    move = engine.Move(player_clicks[0], player_clicks[1], game_state.board)
                    print(move.get_chess_notation())
                    if move in valid_moves:
                        game_state.make_move(move)
                        move_made = True
                    sq_selected = () # Resets the user clicks
                    player_clicks = []

            elif event.type == p.KEYDOWN:
                if event.key == p.K_LEFT:
                    game_state.undo_move()
                    move_made = True

        if move_made:
            valid_moves = game_state.get_valid_moves()
            move_made = False

        draw_game_state(screen, game_state)
        clock.tick(MAX_FPS)
        p.display.flip()

# Loads the images into the ranks and files on the chess board using the images in src/images/
def load_images():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']

    # Assigns size-fitted images to IMAGES list
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load(f"images/{piece}.png"), (SQ_SIZE, SQ_SIZE))

def  draw_game_state(screen, game_state):
    draw_board(screen)
    draw_pieces(screen, game_state.board)

def draw_board(screen):

    for row in range(DIMENSION):
        for col in range(DIMENSION):

            # Set chess board colours
            if (row + col) % 2 == 0:
                colour = WHITE_COLOUR
            else:
                colour = DARK_GRAY_COLOUR

            p.draw.rect(screen, colour, p.Rect(col *SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))

def draw_pieces(screen, board):
    for row in range(DIMENSION):
        for col in range (DIMENSION):
            piece = board[row][col]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))

if __name__ == "__main__":
    main()