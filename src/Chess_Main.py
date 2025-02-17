import pygame as p
from src import Chess_Engine
from src.dimen.dimen import DIMENSION, IMAGES, WIDTH, HEIGHT, SQ_SIZE, COLOURS, MAX_FPS

def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("White"))
    game_state = Chess_Engine.GameState()
    print(game_state.board)
    load_images()
    running = True

    sq_selected = () #tuple i.e. (row, col)
    player_clicks = [] # two tuples - selecting piece to move (row, col), selecting where to move (row, col)
    
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
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
                    move = Chess_Engine.Move(player_clicks[0], player_clicks[1], game_state.board)
                    print(move.get_chess_notation())
                    game_state.make_move(move)
                    sq_selected = () # Resets the user clicks
                    player_clicks = []

        draw_game_state(screen, game_state)
        clock.tick(MAX_FPS)
        p.display.flip()

def load_images():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']

    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load(f"images/{piece}.png"), (SQ_SIZE, SQ_SIZE))

def  draw_game_state(screen, game_state):
    draw_board(screen)
    draw_pieces(screen, game_state.board)

def draw_board(screen):

    for row in range(DIMENSION):
        for col in range(DIMENSION):
            colour = COLOURS[(row + col) % 2]
            p.draw.rect(screen, colour, p.Rect(col *SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))

def draw_pieces(screen, board):
    for row in range(DIMENSION):
        for col in range (DIMENSION):
            piece = board[row][col]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))

if __name__ == "__main__":
    main()