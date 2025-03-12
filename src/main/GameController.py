import pygame as p

from src.main.Board import Board
from src.main.ChessAI import ChessAI
from src.main.GameRules import GameRules
from src.main.MoveValidator import MoveValidator

from src.dimen.dimen import DIMENSION, IMAGES, WIDTH, HEIGHT, SQ_SIZE, MAX_FPS, BACKGROUND_COLOR, BOARD_SQUARE_COLOUR, \
    SQUARE_SELECTED_COLOUR, BOARD_SQUARE_COLOUR_2, SCALER, DOTS

from src.main.Move import Move

class GameController:
    def __init__(self):
        self.screen = None
        self.board = Board()
        self.game_rules = GameRules(self.board)
        self.validator = MoveValidator(self.board, self.game_rules)
        self.ai = ChessAI(self.game_rules, self.board)
        self.clock = p.time.Clock()
        self.player_one = True  # Human white
        self.player_two = False  # Human black


    def load_images(self):
        pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
        for piece in pieces:
            IMAGES[piece] = p.transform.scale(p.image.load(f"images/{piece}.png"), (SQ_SIZE, SQ_SIZE))
        DOTS[0] = p.transform.scale(p.image.load("images/circle-move.png"), (SQ_SIZE // 2, SQ_SIZE // 2))
        DOTS[1] = p.transform.scale(p.image.load("images/circle-capture.png"), (SQ_SIZE, SQ_SIZE))

    def draw_game_state(self, screen, sq_selected, valid_moves):
        self.draw_board(screen, sq_selected, valid_moves)

    def draw_board(self, screen, sq_selected, valid_moves):
        for row in range(DIMENSION):
            for col in range(DIMENSION):
                if (row + col) % 2 == 0:
                    colour = BOARD_SQUARE_COLOUR
                else:
                    colour = BOARD_SQUARE_COLOUR_2
                if (row, col) == sq_selected:
                    colour = SQUARE_SELECTED_COLOUR
                p.draw.rect(screen, colour, p.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))
                self.draw_pieces(screen, row, col)
                if sq_selected:
                    for move in valid_moves:
                        if (move.start_row, move.start_col) == sq_selected:
                            if (row, col) == (move.end_row, move.end_col):
                                if self.board.get_piece(row, col) == "--":
                                    dot_x = col * SQ_SIZE + (SQ_SIZE - DOTS[0].get_width()) // 2
                                    dot_y = row * SQ_SIZE + (SQ_SIZE - DOTS[0].get_height()) // 2
                                    screen.blit(DOTS[0], (dot_x, dot_y))
                                else:
                                    dot_x = col * SQ_SIZE + (SQ_SIZE - DOTS[1].get_width())
                                    dot_y = row * SQ_SIZE + (SQ_SIZE - DOTS[1].get_height())
                                    screen.blit(DOTS[1], (dot_x, dot_y))

    def draw_pieces(self, screen, row, col):
        piece = self.board.get_piece(row, col)
        if piece != "--":
            screen.blit(IMAGES[piece], p.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE // SCALER, SQ_SIZE // SCALER))

    def animate_move(self, screen, clock, sq_selected, valid_moves):
        move = self.game_rules.moveLog[-1]
        d_row = move.end_row - move.start_row
        d_col = move.end_col - move.start_col
        frames_per_square = 10
        frame_count = (abs(d_row) + abs(d_col)) * frames_per_square
        for frame in range(frame_count + 1):
            row = (move.start_row + d_row * (frame / frame_count))
            col = (move.start_col + d_col * (frame / frame_count))
            self.draw_board(screen, sq_selected, valid_moves)
            colour = BOARD_SQUARE_COLOUR if (move.end_row + move.end_col) % 2 == 0 else BOARD_SQUARE_COLOUR_2
            end_square = p.Rect(move.end_col * SQ_SIZE, move.end_row * SQ_SIZE, SQ_SIZE, SQ_SIZE)
            p.draw.rect(screen, colour, end_square)
            screen.blit(IMAGES[move.piece_moved], p.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))
            p.display.flip()
            clock.tick(90)

    def draw_text(self, screen, text):
        font = p.font.SysFont("Helvetica", 32, True, False)
        text_object = font.render(text, True, p.Color("Black"))
        padding = 30
        rect_width = text_object.get_width() + padding
        rect_height = text_object.get_height() + padding
        rect_x = (WIDTH - rect_width) // 2
        rect_y = (HEIGHT - rect_height) // 2
        text_location = p.Rect(rect_x, rect_y, rect_width, rect_height)
        p.draw.rect(screen, BOARD_SQUARE_COLOUR, text_location)
        screen.blit(text_object, (rect_x + padding // 2, rect_y + padding // 2))

    def main(self):
        p.init()
        self.screen = p.display.set_mode((WIDTH, HEIGHT))
        self.screen.fill(BACKGROUND_COLOR)
        valid_moves = self.validator.get_valid_moves()
        move_made = False
        animate = False
        game_over = False
        p.display.set_caption("Chess Game")
        print("Game started.")
        running = True
        sq_selected = ()
        player_clicks = []
        self.load_images()
        while running:
            human_turn = (self.game_rules.whiteToMove and self.player_one) or \
                        (not self.game_rules.whiteToMove and self.player_two)
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
                            move = Move(player_clicks[0], player_clicks[1], self.board)
                            for i in range(len(valid_moves)):
                                if move == valid_moves[i]:
                                    self.game_rules.make_move(valid_moves[i])
                                    move_made = True
                                    animate = True
                                    sq_selected = ()
                                    player_clicks = []
                            if not move_made:
                                player_clicks = [sq_selected]

                elif event.type == p.KEYDOWN:
                    if event.key == p.K_LEFT:
                        self.game_rules.undo_move()
                        move_made = True
                        animate = False
                        game_over = False

                    # Reset the board
                    if event.key == p.K_r:
                        self.board = Board()
                        self.game_rules = GameRules(self.board)
                        self.validator = MoveValidator(self.board, self.game_rules)
                        self.ai = ChessAI(self.game_rules, self.board)
                        valid_moves = self.validator.get_valid_moves()
                        player_clicks = []
                        game_over = False
                        move_made = False
                        animate = False

            if not game_over and not human_turn:
                ai_move = self.ai.find_best_move(valid_moves)
                if ai_move:
                    print(f"AI chose: {ai_move.get_chess_notation()}")
                else:
                    print(f"AI chose: {ai_move.get_chess_notation()}")
                if ai_move is None:
                    ai_move = self.ai.find_random_move(valid_moves)
                self.game_rules.make_move(ai_move)
                move_made = True
                animate = True
            if move_made:
                if animate:
                    self.animate_move(self.screen, self.clock, sq_selected, valid_moves)
                valid_moves = self.validator.get_valid_moves()
                move_made = False
                animate = False
            self.draw_game_state(self.screen, sq_selected, valid_moves)
            if self.game_rules.check_mate:
                game_over = True
                if self.game_rules.whiteToMove:
                    self.draw_text(self.screen, "Black wins by checkmate")
                else:
                    self.draw_text(self.screen, "White wins by checkmate")
            elif self.game_rules.stale_mate:
                game_over = True
                self.draw_text(self.screen, "Draw - stalemate")

            self.clock.tick(MAX_FPS)
            p.display.flip()