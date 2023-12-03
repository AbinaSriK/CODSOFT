import copy
import sys
import pygame
import random
import numpy as np
wid = 500
height = 500
R= 3
C = 3
size = wid // C
LW = 10
CW = 10
CROSS = 15
RADIUS = size // 4
OFFSET = 50
BG_COLOR = (128,128,128)
LINE_COLOR = (192,192,192)
CIRC_COLOR = (0,0,0)
CROSS_COLOR = (66, 66, 66)
pygame.init()
screen = pygame.display.set_mode((wid, height))
pygame.display.set_caption('TIC TAC TOE')
screen.fill(BG_COLOR)
class Board:
    def __init__(self):
        self.squares = np.zeros((R, C))
        self.empty_sqrs = self.squares  # [squares]
        self.marked_sqrs = 0
    def final_state(self, show=False):
        for col in range(C):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0:
                if show:
                    color = CIRC_COLOR if self.squares[0][col] == 2 else CROSS_COLOR
                    iPos = (col * size + size // 2, 20)
                    fPos = (col * size + size // 2, height - 20)
                    pygame.draw.line(screen, color, iPos, fPos, LW)
                return self.squares[0][col]
        for row in range(R):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                if show:
                    color = CIRC_COLOR if self.squares[row][0] == 2 else CROSS_COLOR
                    iPos = (20, row * size + size // 2)
                    fPos = (wid - 20, row * size + size // 2)
                    pygame.draw.line(screen, color, iPos, fPos, LW)
                return self.squares[row][0]
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            if show:
                color = CIRC_COLOR if self.squares[1][1] == 2 else CROSS_COLOR
                iPos = (20, 20)
                fPos = (wid - 20, height - 20)
                pygame.draw.line(screen, color, iPos, fPos, CROSS)
            return self.squares[1][1]
        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0:
            if show:
                color = CIRC_COLOR if self.squares[1][1] == 2 else CROSS_COLOR
                iPos = (20, height - 20)
                fPos = (wid - 20, 20)
                pygame.draw.line(screen, color, iPos, fPos, CROSS)
            return self.squares[1][1]
        return 0
    def mark_sqr(self, row, col, player):
        self.squares[row][col] = player
        self.marked_sqrs += 1
    def empty_sqr(self, row, col):
        return self.squares[row][col] == 0
    def get_empty_sqrs(self):
        empty_sqrs = []
        for row in range(R):
            for col in range(C):
                if self.empty_sqr(row, col):
                    empty_sqrs.append((row, col))
        return empty_sqrs
    def isfull(self):
        return self.marked_sqrs == 9
    def isempty(self):
        return self.marked_sqrs == 0
class AI:
    def __init__(self, level=1, player=2):
        self.level = level
        self.player = player
    def rnd(self, board):
        empty_sqrs = board.get_empty_sqrs()
        idx = random.randrange(0, len(empty_sqrs))
        return empty_sqrs[idx]
    def minimax(self, board, maximizing):
        case = board.final_state()
        if case == 1:
            return 1, None  # eval, move
        if case == 2:
            return -1, None
        elif board.isfull():
            return 0, None
        if maximizing:
            max_eval = -100
            best_move = None
            empty_sqrs = board.get_empty_sqrs()
            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, 1)
                eval = self.minimax(temp_board, False)[0]
                if eval > max_eval:
                    max_eval = eval
                    best_move = (row, col)
            return max_eval, best_move
        elif not maximizing:
            min_eval = 100
            best_move = None
            empty_sqrs = board.get_empty_sqrs()
            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, self.player)
                eval = self.minimax(temp_board, True)[0]
                if eval < min_eval:
                    min_eval = eval
                    best_move = (row, col)
            return min_eval, best_move
    def eval(self, main_board):
        if self.level == 0:

            eval = 'random'
            move = self.rnd(main_board)
        else:

            eval, move = self.minimax(main_board, False)
        return move
class Game:
    def __init__(self):
        self.board = Board()
        self.ai = AI()
        self.player = 1
        self.gamemode = 'ai'
        self.running = True
        self.show_lines()
    def show_lines(self):
        screen.fill(BG_COLOR)
        pygame.draw.line(screen, LINE_COLOR, (size, 0), (size, height), LW)
        pygame.draw.line(screen, LINE_COLOR, (wid - size, 0), (wid - size, height), LW)
        pygame.draw.line(screen, LINE_COLOR, (0, size), (wid, size), LW)
        pygame.draw.line(screen, LINE_COLOR, (0, height - size), (wid, height - size), LW)
    def draw_fig(self, row, col):
        if self.player == 1:
            start_desc = (col * size + OFFSET, row * size + OFFSET)
            end_desc = (col * size + size - OFFSET, row * size + size - OFFSET)
            pygame.draw.line(screen, CROSS_COLOR, start_desc, end_desc, CROSS)

            start_asc = (col * size + OFFSET, row * size + size - OFFSET)
            end_asc = (col * size + size - OFFSET, row * size + OFFSET)
            pygame.draw.line(screen, CROSS_COLOR, start_asc, end_asc, CROSS)

        elif self.player == 2:
            center = (col * size + size // 2, row * size + size // 2)
            pygame.draw.circle(screen, CIRC_COLOR, center, RADIUS, CW)
    def make_move(self, row, col):
        self.board.mark_sqr(row, col, self.player)
        self.draw_fig(row, col)
        self.next_turn()
    def next_turn(self):
        self.player = self.player % 2 + 1
    def isover(self):
        return self.board.final_state(show=True) != 0 or self.board.isfull()

    def reset(self):
        self.__init__()
def main():
    game = Game()
    board = game.board
    ai = game.ai

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                row = pos[1] // size
                col = pos[0] // size
                if board.empty_sqr(row, col) and game.running:
                    game.make_move(row, col)
                    if game.isover():
                        game.running = False
        if game.gamemode == 'ai' and game.player == ai.player and game.running:
            pygame.display.update()
            row, col = ai.eval(board)
            game.make_move(row, col)
            if game.isover():
                game.running = False
        pygame.display.update()
main()
