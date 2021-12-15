import random


class Board:
    def __init__(self, x_list, o_list):
        self.board = [" " for x in range(10)]
        self.x_list = x_list
        self.o_list = o_list
        # populating the board with the moves
        for x in x_list:
            self.board[x] = "x"
        for o in o_list:
            self.board[o] = "o"

    def is_a_win(self, the_board, the_letter):
        result = (the_board[1] == the_letter and the_board[4] == the_letter and the_board[7] == the_letter) or \
                 (the_board[1] == the_letter and the_board[5] == the_letter and the_board[9] == the_letter) or \
                 (the_board[1] == the_letter and the_board[2] == the_letter and the_board[3] == the_letter) or \
                 (the_board[2] == the_letter and the_board[5] == the_letter and the_board[8] == the_letter) or \
                 (the_board[4] == the_letter and the_board[5] == the_letter and the_board[6] == the_letter) or \
                 (the_board[3] == the_letter and the_board[6] == the_letter and the_board[9] == the_letter) or \
                 (the_board[3] == the_letter and the_board[5] == the_letter and the_board[7] == the_letter) or \
                 (the_board[7] == the_letter and the_board[8] == the_letter and the_board[9] == the_letter)
        return result

    # pick a random move for computer to use later
    def random_move(self, move_list):
        return random.choice(move_list)

    def computer_move(self):
        possible_moves = []

        # collects all the position that aren't yet filled
        for index, x_or_o in enumerate(self.board):
            if x_or_o == " " and index != 0:
                possible_moves.append(index)

        if len(possible_moves) == 0:
            return -1

        # identify a winning position and plays
        # checks if it can block x from winning
        for let in ["o", "x"]:
            for i in possible_moves:
                board_copy = self.board.copy()
                board_copy[i] = let
                if self.is_a_win(board_copy, let):
                    self.board[i] = 'o'
                    move = i
                    return move

        # plays in middle
        if 5 in possible_moves:
            move = 5
            return move

        # check if any of the possible movers are corners
        open_corners = [i for i in possible_moves if i in [1, 3, 7, 9]]
        if len(open_corners) > 0:
            move = self.random_move(open_corners)
            return move

        # if any edges open
        open_edge = [i for i in possible_moves if i in [2, 4, 6, 8]]
        if len(open_edge) > 0:
            move = self.random_move(open_edge)
            return move
