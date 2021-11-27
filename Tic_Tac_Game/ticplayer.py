import random
from ticboard import Board


class Player(Board):
    def __init__(self, name = "Anonymous", computer_player = False):
        self.name = name
        self.computer_player = computer_player
        self.letter = "X"

    def get_move(self):
        move_answer = input("Enter the position you would like to play(1-9): ")
        return move_answer

    def human_move(self):
        flag = True
        while flag:
            move = self.get_move()
            try:
                move = int(move)
                if (move > 0) and (move < 10):
                    if self.space_available(move):
                        flag = False
                        self.make_move(self.letter, move)
                    else:
                        print("Sorry, this space is not available to play i")
                else:
                    print("Please enter a position within the range (1-9)")
            except ValueError:
                print("Please enter a number!")
        return move

    def random_move(self, move_list):
        return random.choice(move_list)

    def computer_move(self):
        possible_moves = []

        # collects all the position that aren't yet filled
        for index, x_or_o in enumerate(Board.board):
            if x_or_o == " " and index != 0:
                possible_moves.append(index)

        move = 0

        # if move we can make that will result in a win and if opponent's move can result in win
        # make the move
        for let in ["O", "X"]:
            for i in possible_moves:
                board_copy = self.board.copy()
                board_copy[i] = let
                if self.is_a_win(board_copy, let):
                    move = i
                    return move

        # play in middle
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

