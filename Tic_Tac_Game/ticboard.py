import random


class Board:


    def __init__(self, x_list, o_list):
        self.board = [" " for x in range(10)]
        self.x_list = x_list
        self.o_list = o_list

        for x in x_list:
            self.board[x] = "x"

        for o in o_list:
            self.board[o] = "o"

    def is_a_win(self, the_letter):
        result = (self.board[1] == the_letter and self.board[4] == the_letter and self.board[7] == the_letter) or \
                 (self.board[1] == the_letter and self.board[5] == the_letter and self.board[9] == the_letter) or \
                 (self.board[1] == the_letter and self.board[2] == the_letter and self.board[3] == the_letter) or \
                 (self.board[2] == the_letter and self.board[5] == the_letter and self.board[8] == the_letter) or \
                 (self.board[4] == the_letter and self.board[5] == the_letter and self.board[6] == the_letter) or \
                 (self.board[3] == the_letter and self.board[6] == the_letter and self.board[9] == the_letter) or \
                 (self.board[3] == the_letter and self.board[5] == the_letter and self.board[7] == the_letter) or \
                 (self.board[7] == the_letter and self.board[8] == the_letter and self.board[9] == the_letter)
        return result

    def random_move(self, move_list):
        return random.choice(move_list)

    def computer_move(self):
        possible_moves = []

        # collects all the position that aren't yet filled
        for index, x_or_o in enumerate(self.board):
            if x_or_o == " " and index != 0:
                possible_moves.append(index)

        print("printing list of possible moves: ", possible_moves)
        if len(possible_moves) == 0:
            return -1

        for i in possible_moves:
            board_copy = self.board.copy()
            board_copy[i] = 'o'
            if self.is_a_win(board_copy):
                move = i
                self.board[i] = 'o'
                return move

        # play in middle
        if 5 in possible_moves:
            move = 5
            self.board[5] = 'o'
            return move

        # check if any of the possible movers are corners
        open_corners = [i for i in possible_moves if i in [1, 3, 7, 9]]
        if len(open_corners) > 0:
            move = self.random_move(open_corners)
            self.board[move] = 'o'
            return move

        # if any edges open
        open_edge = [i for i in possible_moves if i in [2, 4, 6, 8]]
        if len(open_edge) > 0:
            move = self.random_move(open_edge)
            self.board[move] = 'o'
            return move

