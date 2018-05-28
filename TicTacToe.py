from enum import Enum
import math


class GameState(Enum):
    CONTINUE = 0
    WON = 1
    TIE = 2


class Game:
    def __init__(self):
        self.board = [[None, None, None], [
            None, None, None], [None, None, None]]
        self.choice = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
        self.turn = False
        self.gameState = GameState.CONTINUE

    def start_game(self):
        while self.gameState == GameState.CONTINUE:
            self.turn = not self.turn
            print('Current board is')
            self.show_game_state()
            if self.turn:
                print("Circle's Turn")
            else:
                print("Cross's Turn")
            print("Choose next move.")
            self.show_pos_choice()
            pos = int(input())
            while not self.valid_move(pos):
                print('Cell is already taken, or out of range!')
                pos = int(input())
            self.place_move(pos)
            if self.has_ended():
                if self.gameState == GameState.TIE:
                    print("Tie!")
                elif self.turn:
                    print("Circle won!")
                else:
                    print("Cross won!")
                return

    def show_game_state(self):
        print(self.board)

    def show_pos_choice(self):
        print(self.choice)

    def valid_move(self, pos):
        if pos < 0 or pos > 8:
            return False
        row = math.floor(pos // 3)
        col = pos % 3
        return self.board[row][col] == None

    def place_move(self, pos):
        row = math.floor(pos // 3)
        col = pos % 3
        if self.board[row][col] == None:
            self.board[row][col] = self.turn
        else:
            print('Cell is already taken!')
            return False

    def has_ended(self):
        board = self.board
        for r in range(3):
            if board[r][0] == board[r][1] == board[r][2] and board[r][0] != None:
                self.gameState = GameState.WON
                return True

        for c in range(3):
            if board[0][c] == board[1][c] == board[2][c] and board[0][c] != None:
                self.gameState = GameState.WON
                return True

        if board[0][0] == board[1][1] == board[2][2] and board[0][0] != None:
            self.gameState = GameState.WON
            return True

        if board[2][0] == board[1][1] == board[0][2] and board[2][0] != None:
            self.gameState = GameState.WON
            return True

        tie = True
        for r in range(3):
            for c in range(3):
                if board[r][c] == None:
                    tie = False
        if tie:
            self.gameState = GameState.TIE
            return True

        return False


g = Game()
g.start_game()
