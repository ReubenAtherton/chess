import pygame as p

from src.dimen.dimen import DIMENSION, IMAGES, WIDTH, HEIGHT, SQ_SIZE, MAX_FPS, BACKGROUND_COLOR, SQUARE_COLOUR, \
    SQUARE_SELECTED_COLOUR, SQUARE_COLOUR_2, SCALER, DOTS
from src.main.GameState import GameState
from src.main.Move import Move


def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(BACKGROUND_COLOR)
    game_state = GameState()
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
                    move = Move(player_clicks[0], player_clicks[1], game_state.board)
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

        draw_game_state(screen, game_state, sq_selected, valid_moves)
        clock.tick(MAX_FPS)
        p.display.flip()

# Loads the images into the ranks and files on the chess board using the images in src/images/
def load_images():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']

    # Assigns size-fitted images to IMAGES list
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load(f"images/{piece}.png"), (SQ_SIZE, SQ_SIZE))

    DOTS[0] = p.transform.scale(p.image.load("images/circle-move.png"),(SQ_SIZE // 2, SQ_SIZE // 2))
    DOTS[1] = p.transform.scale(p.image.load("images/circle-capture.png"), (SQ_SIZE, SQ_SIZE))

def  draw_game_state(screen, game_state, sq_selected, valid_moves):
    draw_board(screen, game_state.board, sq_selected, valid_moves)

def draw_board(screen, board, sq_selected, valid_moves):
    # Step 1: Draw chess board
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            # Set board colours
            if (row + col) % 2 == 0:
                colour = SQUARE_COLOUR
            else:
                colour = SQUARE_COLOUR_2

            # Highlight selected square
            if (row, col) == sq_selected:
                colour = SQUARE_SELECTED_COLOUR

            # Draw board and pieces
            p.draw.rect(screen, colour, p.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))
            draw_pieces(screen, board, row, col)

            # Draw top layer - valid moves, valid captures
            if sq_selected:
                for move in valid_moves:
                    if (move.start_row, move.start_col) == sq_selected:
                        if (row, col) == (move.end_row, move.end_col):

                            # Empty tile
                            if board[row][col] == "--":
                                dot_x = col * SQ_SIZE + (SQ_SIZE - DOTS[0].get_width()) // 2
                                dot_y = row * SQ_SIZE + (SQ_SIZE - DOTS[0].get_height()) // 2
                                screen.blit(DOTS[0], (dot_x, dot_y))

                            # Occupied tile
                            else:
                                dot_x = col * SQ_SIZE + (SQ_SIZE - DOTS[1].get_width())
                                dot_y = row * SQ_SIZE + (SQ_SIZE - DOTS[1].get_height())
                                screen.blit(DOTS[1], (dot_x, dot_y))

def draw_pieces(screen, board, row, col):
            piece = board[row][col]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE // SCALER, SQ_SIZE //SCALER))

def draw_valid_moves():
    pass

if __name__ == "__main__":
    main()