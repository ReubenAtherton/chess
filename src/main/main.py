import pygame as p
import ChessAI as ai
from src.main.Board import Board

from src.dimen.dimen import DIMENSION, IMAGES, WIDTH, HEIGHT, SQ_SIZE, MAX_FPS, BACKGROUND_COLOR, BOARD_SQUARE_COLOUR, \
    SQUARE_SELECTED_COLOUR, BOARD_SQUARE_COLOUR_2, SCALER, DOTS
from src.main.GameState import GameState
from src.main.Move import Move

def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(BACKGROUND_COLOR)

    board = Board()

    game_state = GameState(board)
    valid_moves = game_state.get_valid_moves()
    move_made = False # Flag variable for when a move is made
    animate = False
    game_over = False

    load_images()
    running = True

    sq_selected = () #tuple i.e. (row, col)
    player_clicks = [] # two tuples - selecting piece to move (row, col), selecting where to move (row, col)

    player_one = True # if human playing white then True, if AI is playing then False
    player_two = False # same as above but for black

    while running:
        human_turn = (game_state.whiteToMove and player_one) or (not game_state.whiteToMove and player_two)
        for event in p.event.get():
            if event.type == p.QUIT:
                running = False

            elif event.type == p.MOUSEBUTTONDOWN:
                if not game_over and human_turn:
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
                        move = Move(player_clicks[0], player_clicks[1], game_state.board)   # Create the move

                        for i in range(len(valid_moves)):   # Check the move is a valid move
                            if move == valid_moves[i]:
                                game_state.make_move(valid_moves[i])
                                move_made = True
                                animate = True
                                sq_selected = ()    # Resets the user clicks
                                player_clicks = []

                        if not move_made:
                            player_clicks = [sq_selected]


            elif event.type == p.KEYDOWN:
                # Undo move
                if event.key == p.K_LEFT:
                    game_state.undo_move()
                    move_made = True
                    animate = False
                    game_over = False  # Reset game over flag when undoing a move

                # Reset board
                if event.key == p.K_r:
                    game_state = GameState()
                    valid_moves = game_state.get_valid_moves()  # Properly reset valid moves
                    player_clicks = []
                    game_over = False  # Reset game over flag
                    move_made = False
                    animate = False

        # AI move finder logic
        if not game_over and not human_turn:
            ai_move = ai.find_best_move(game_state, valid_moves)
            if ai_move is None:
                print("true")
                ai_move = ai.find_random_move(valid_moves)
            game_state.make_move(ai_move)
            move_made = True
            animate = True

        if move_made:
            if animate:
                animate_move(game_state, screen, clock, sq_selected, valid_moves)
            valid_moves = game_state.get_valid_moves()
            move_made = False
            animate = False

        draw_game_state(screen, game_state, sq_selected, valid_moves)

        if game_state.check_mate:
            game_over = True
            if game_state.whiteToMove:
                draw_text(screen, "Black wins by checkmate")
            else:
                draw_text(screen, "White wins by checkmate")

        elif game_state.stale_mate:
            game_over = True
            draw_text(screen, "Draw - stalemate")

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

def draw_game_state(screen, game_state, sq_selected, valid_moves):
    draw_board(screen, game_state.board, sq_selected, valid_moves)

def draw_board(screen, board, sq_selected, valid_moves):
    # Step 1: Draw chess board
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            # Set board colours
            if (row + col) % 2 == 0:
                colour = BOARD_SQUARE_COLOUR
            else:
                colour = BOARD_SQUARE_COLOUR_2

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

                            # Show empty tile to move onto
                            if board.get_piece(row, col) == "--":
                                dot_x = col * SQ_SIZE + (SQ_SIZE - DOTS[0].get_width()) // 2
                                dot_y = row * SQ_SIZE + (SQ_SIZE - DOTS[0].get_height()) // 2
                                screen.blit(DOTS[0], (dot_x, dot_y))

                            # Show occupied tile to capture
                            else:
                                dot_x = col * SQ_SIZE + (SQ_SIZE - DOTS[1].get_width())
                                dot_y = row * SQ_SIZE + (SQ_SIZE - DOTS[1].get_height())
                                screen.blit(DOTS[1], (dot_x, dot_y))

def draw_pieces(screen, board, row, col):
        piece = board.get_piece(row, col)
        if piece != "--":
            screen.blit(IMAGES[piece], p.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE // SCALER, SQ_SIZE //SCALER))

def animate_move(game_state, screen, clock, sq_selected, valid_moves):
    move = game_state.moveLog[-1]  # Get the last move made
    board = game_state.board

    d_row = move.end_row - move.start_row
    d_col = move.end_col - move.start_col
    frames_per_square = 10
    frame_count = (abs(d_row) + abs(d_col)) * frames_per_square  # Fix precedence

    for frame in range(frame_count + 1):
        row = (move.start_row + d_row * (frame / frame_count))
        col = (move.start_col + d_col * (frame / frame_count))

        draw_board(screen, board, sq_selected, valid_moves)  # Redraw the board

        # Clear the piece from its last position
        colour = BOARD_SQUARE_COLOUR if (move.end_row + move.end_col) % 2 == 0 else BOARD_SQUARE_COLOUR_2
        end_square = p.Rect(move.end_col * SQ_SIZE, move.end_row * SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, colour, end_square)

        # Draw the moving piece
        screen.blit(IMAGES[move.piece_moved], p.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))

        p.display.flip()
        clock.tick(90)

def draw_text(screen, text):
    font = p.font.SysFont("Helvetica", 32, True, False)
    text_object = font.render(text, True, p.Color("Black"))  # Render with anti-aliasing

    padding = 30  # Padding around the text inside the rectangle
    rect_width = text_object.get_width() + padding
    rect_height = text_object.get_height() + padding

    # Center the rectangle on the screen
    rect_x = (WIDTH - rect_width) // 2
    rect_y = (HEIGHT - rect_height) // 2

    text_location = p.Rect(rect_x, rect_y, rect_width, rect_height)

    # Draw the rectangle
    p.draw.rect(screen, p.Color(BOARD_SQUARE_COLOUR), text_location)

    # Center the text inside the rectangle
    text_x = rect_x + padding // 2
    text_y = rect_y + padding // 2

    screen.blit(text_object, (text_x, text_y))

if __name__ == "__main__":
    main()