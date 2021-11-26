class Board:
    board = [" " for x in range(10)]

    @classmethod
    def board_board(cls):
        return cls.board

    @classmethod
    def clear_board(cls):
        return cls.board.clear()

    def display_board(self):
        print("      |      |")
        print(" " + self.board[1] + "    | " + self.board[2] + "    | " + self.board[3])
        print("      |      |")
        print("-" * 20)
        print("      |      |")
        print(" " + self.board[4] + "    | " + self.board[5] + "    | " + self.board[6])
        print("      |      |")
        print("-" * 20)
        print("      |      |")
        print(" " + self.board[7] + "    | " + self.board[8] + "    | " + self.board[9])
        print("      |      |")

    def space_available(self, position):
        available = self.board[position] == " "
        return available

    def no_space_on_board(self):
        if self.board.count(" ") > 1:
            return False
        else:
            return True

    def is_a_win(self, board_space, the_letter):
        result = (board_space[1] == the_letter and board_space[4] == the_letter and board_space[7] == the_letter) or \
                 (board_space[1] == the_letter and board_space[5] == the_letter and board_space[9] == the_letter) or \
                 (board_space[1] == the_letter and board_space[2] == the_letter and board_space[3] == the_letter) or \
                 (board_space[2] == the_letter and board_space[5] == the_letter and board_space[8] == the_letter) or \
                 (board_space[4] == the_letter and board_space[5] == the_letter and board_space[6] == the_letter) or \
                 (board_space[3] == the_letter and board_space[6] == the_letter and board_space[9] == the_letter) or \
                 (board_space[3] == the_letter and board_space[5] == the_letter and board_space[7] == the_letter) or \
                 (board_space[7] == the_letter and board_space[8] == the_letter and board_space[9] == the_letter)
        return result

    def make_move(self, x_or_o, position):
        self.board[position] = x_or_o

