import unittest
from FINALPROJECT.games.ticboard import Board


class TestBoard(unittest.TestCase):

    # test if identifies if o wins
    def test_o_wins(self):
        # b1, b2 ..etc represents different instance of boards
        b1, b2 = Board([2, 9, 6], [1, 4, 7]), Board([2, 3, 6], [1, 5, 9])
        b3, b4 = Board([5, 9, 6], [1, 2, 3]), Board([1, 9, 6], [2, 5, 8])
        b5, b6 = Board([1, 9, 8], [4, 5, 6]), Board([1, 4, 7], [3, 6, 9])
        b7, b8 = Board([1, 9, 6], [3, 5, 7]), Board([1, 3, 6], [7, 8, 9])

        b9, b10 = Board([2, 9, 6], [3, 4, 7]), Board([2, 3, 6], [4, 5, 9])
        b11, b12 = Board([2, 9, 6], [5, 2, 3]), Board([1, 9, 6], [3, 5, 8])
        b13, b14 = Board([1, 9, 6], [7, 5, 6]), Board([1, 4, 7], [8, 6, 9])
        b15, b16 = Board([1, 9, 6], [2, 5, 7]), Board([1, 3, 6], [5, 8, 9])

        self.assertEqual(b1.is_a_win(b1.board, "o"), True)
        self.assertEqual(b2.is_a_win(b2.board, "o"), True)
        self.assertEqual(b3.is_a_win(b3.board, "o"), True)
        self.assertEqual(b4.is_a_win(b4.board, "o"), True)
        self.assertEqual(b5.is_a_win(b5.board, "o"), True)
        self.assertEqual(b6.is_a_win(b6.board, "o"), True)
        self.assertEqual(b7.is_a_win(b7.board, "o"), True)
        self.assertEqual(b8.is_a_win(b8.board, "o"), True)

        # test it returns false if no wins for o
        self.assertEqual(b9.is_a_win(b9.board, "o"), False)
        self.assertEqual(b10.is_a_win(b10.board, "o"), False)
        self.assertEqual(b11.is_a_win(b11.board, "o"), False)
        self.assertEqual(b12.is_a_win(b12.board, "o"), False)
        self.assertEqual(b13.is_a_win(b13.board, "o"), False)
        self.assertEqual(b14.is_a_win(b14.board, "o"), False)
        self.assertEqual(b15.is_a_win(b15.board, "o"), False)
        self.assertEqual(b16.is_a_win(b16.board, "o"), False)

    # test to identify if x wins
    def test_x_wins(self):
        b1, b2 = Board([1, 4, 7], [5, 9, 6]), Board([1, 5, 9], [2, 3, 6])
        b3, b4 = Board([1, 2, 3], [5, 9, 6]), Board([2, 5, 8], [1, 9, 6])
        b5, b6 = Board([4, 5, 6], [1, 9, 8]), Board([3, 6, 9], [1, 4, 7])
        b7, b8 = Board([3, 5, 7], [1, 9, 6]), Board([7, 8, 9], [1, 3, 6])

        b9, b10 = Board([3, 4, 7], [2, 9, 6]), Board([4, 5, 9], [2, 3, 6])
        b11, b12 = Board([5, 2, 3], [2, 9, 6]), Board([3, 5, 8], [1, 9, 6])
        b13, b14 = Board([7, 5, 6], [1, 9, 6]), Board([8, 6, 9], [1, 4, 7])
        b15, b16 = Board([2, 5, 7], [1, 9, 6]), Board([5, 8, 9], [1, 3, 6])

        self.assertEqual(b1.is_a_win(b1.board, "x"), True)
        self.assertEqual(b2.is_a_win(b2.board, "x"), True)
        self.assertEqual(b3.is_a_win(b3.board, "x"), True)
        self.assertEqual(b4.is_a_win(b4.board, "x"), True)
        self.assertEqual(b5.is_a_win(b5.board, "x"), True)
        self.assertEqual(b6.is_a_win(b6.board, "x"), True)
        self.assertEqual(b7.is_a_win(b7.board, "x"), True)
        self.assertEqual(b8.is_a_win(b8.board, "x"), True)

        # test it returns false if no wins for x
        self.assertEqual(b9.is_a_win(b9.board, "x"), False)
        self.assertEqual(b10.is_a_win(b10.board, "x"), False)
        self.assertEqual(b11.is_a_win(b11.board, "x"), False)
        self.assertEqual(b12.is_a_win(b12.board, "x"), False)
        self.assertEqual(b13.is_a_win(b13.board, "x"), False)
        self.assertEqual(b14.is_a_win(b14.board, "x"), False)
        self.assertEqual(b15.is_a_win(b15.board, "x"), False)
        self.assertEqual(b16.is_a_win(b16.board, "x"), False)

    # test to check if it'll make middle move as first move
    def test_comp_middle_move(self):
        self.assertEqual(Board([1], []).computer_move(), 5)
        self.assertEqual(Board([2], []).computer_move(), 5)
        self.assertEqual(Board([3], []).computer_move(), 5)
        self.assertEqual(Board([4], []).computer_move(), 5)
        self.assertNotEqual(Board([5], []).computer_move(), 5)  # if x plays in middle first


    # test if it'll block a wining move if possible
    def test_block_move(self):
        self.assertEqual(Board([1, 4], [5]).computer_move(), 7)
        self.assertEqual(Board([5, 9], [3]).computer_move(), 1)
        self.assertEqual(Board([1, 2], [5]).computer_move(), 3)
        self.assertEqual(Board([5, 2], [1]).computer_move(), 8)
        self.assertEqual(Board([5, 6], [7]).computer_move(), 4)
        self.assertEqual(Board([3, 6], [5]).computer_move(), 9)
        self.assertEqual(Board([5, 7], [9]).computer_move(), 3)
        self.assertEqual(Board([7, 9], [5]).computer_move(), 8)



if __name__ == "__main__":
    unittest.main()

