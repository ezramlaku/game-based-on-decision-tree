import sys
import pygame
import random
import copy
import numpy as np

WIDTH=600
HIGHT=600
ROWS = 3
COLS = 3
SQSIZE = WIDTH // COLS
LINE_WIDTH=15
CIRC_WIDTH=15
CROSS_WIDTH=20
OFFSET = 50
RADIUS = SQSIZE // 4
CROSS_COLOR =(66, 66, 66)
CIRC_COLOR =(100, 100, 100)
BG_COLOR = (50, 50, 50)
LINE_COLOR=(0,0,0)
pygame.init()
screen = pygame.display.set_mode((WIDTH, HIGHT))
pygame.display.set_caption("TIC TAC TOE")
screen.fill(BG_COLOR)

class Board:
    def __init__(self):
        self.squares = np.zeros((ROWS, COLS))
        self.empty_sqrs = self.squares
        self.mark_sqrs = 0

    def final_state(self):
        '''
        :return: 0 if there is no win yet
        :return: 1 if player 1 wins
        :return: 2 if player 2 wins
        '''
        #vertical wins
        for col in range(COLS):
            if self.squares[0][col] == self.squares[1][col]==self.squares[2][col] != 0:
                return self.squares[0][col]
        # horizontal wins
        for row in range(ROWS):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                return self.squares[row][0]
        # diagonal wins
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            return self.squares[1][1]
        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0:
            return self.squares[1][1]

        # no win
        return 0

    def mark_sqr(self, row, col, player):
        self.squares[row][col] = player
        self.mark_sqrs += 1
    def empty_sqr(self, row, col):
        return self.squares[row][col] == 0
    def isfull(self):
        return self.mark_sqrs == 9 # T or F

    def get_empty_sqrs(self):
        empty_sqrs= []
        for row in range(ROWS):
            for col in range(COLS):
                if self.empty_sqr(row, col):
                    empty_sqrs.append((row, col))
        return empty_sqrs


class AI:
    def __init__(self):
        self.player = 2

    def minimax(self, board, maximizing):
        # terminal case
        case = board.final_state()
        # player 1 wins
        if case == 1:
            return 1, None
        # player 2 wins
        if case == 2:
            return -1, None
        elif board.isfull():
            return 0, None
        if maximizing:
            max_eval = -2
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
            min_eval = 2
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
        # minimax algo choice
        eval, move = self.minimax(main_board, False)
        print(f'AI has chosen to mark the square in pos {move} with an eval of: {eval}')
        return move  # row, col





class Game:
    def __init__(self):
        self.board = Board()
        self.ai = AI()
        self.player = 1 # 1 Cross 2 Circles
        self.running =True
        self.show_line()
    def reset(self):
        self.__init__()

    def isover(self):
        return( self.board.final_state() != 0 or self.board.isfull())


    def draw_fig(self,row,col):
        if self.player == 1:
            # draw cross
            # desc line
            start_desc =(col * SQSIZE + OFFSET,row * SQSIZE + OFFSET)
            end_desc = (col * SQSIZE + SQSIZE - OFFSET , row * SQSIZE + SQSIZE - OFFSET)
            pygame.draw.line(screen,CROSS_COLOR,start_desc,end_desc,CROSS_WIDTH)
            # asc line
            start_asc= (col * SQSIZE + OFFSET, row * SQSIZE + SQSIZE - OFFSET)
            end_asc = (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + OFFSET)
            pygame.draw.line(screen, CROSS_COLOR, start_asc, end_asc, CROSS_WIDTH)

        elif self.player == 2:
            # draw Circle
            center =(col * SQSIZE + SQSIZE // 2,row * SQSIZE + SQSIZE // 2)
            pygame.draw.circle(screen,CIRC_COLOR,center,RADIUS,CIRC_WIDTH)
    def next_turn(self):
        if self.player == 1:
            self.player = 2
        else:
            self.player = 1

    def show_line(self):
        screen.fill(BG_COLOR)
        # vertical
        pygame.draw.line(screen,LINE_COLOR,(SQSIZE,0),(SQSIZE,HIGHT),LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (WIDTH-SQSIZE, 0), (WIDTH-SQSIZE, HIGHT), LINE_WIDTH)
        # horizontal
        pygame.draw.line(screen, LINE_COLOR, (0, SQSIZE), (WIDTH, SQSIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (0, HIGHT-SQSIZE), (WIDTH,  HIGHT-SQSIZE), LINE_WIDTH)


# mainloop
game = Game()
board = game.board
ai = game.ai


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                game.reset()
                board = game.board
                ai = game.ai
            if event.key == pygame.K_q:
                pygame.quit()
                sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            row = pos[1] // SQSIZE
            col = pos[0] // SQSIZE

            if board.empty_sqr(row,col) and game.running:
                board.mark_sqr(row,col,game.player)
                game.draw_fig(row,col)
               # print(game.player)
                print(board.squares)
                game.next_turn()
                if game.isover():
                    game.running = False



    if game.player == ai.player and game.running:
        #update the screen
        pygame.display.update()

        # ai methods
        row, col = ai.eval(board)

        board.mark_sqr(row, col, game.player)
        game.draw_fig(row, col)
       # print(game.player)
        print(board.squares)
        game.next_turn()
        if game.isover():
            game.running = False



    pygame.display.update()


