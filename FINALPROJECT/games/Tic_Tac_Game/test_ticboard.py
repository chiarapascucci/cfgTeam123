import unittest
from ticboard import Board


class TestBoard(unittest.TestCase):

    # test if identifies if o wins
    def test_o_wins(self):
        self.assertEqual(Board([2, 9, 6], [1, 4, 7]).is_a_win("o"), True)
        self.assertEqual(Board([2, 3, 6], [1, 5, 9]).is_a_win("o"), True)
        self.assertEqual(Board([5, 9, 6], [1, 2, 3]).is_a_win("o"), True)
        self.assertEqual(Board([1, 9, 6], [2, 5, 8]).is_a_win("o"), True)
        self.assertEqual(Board([1, 9, 8], [4, 5, 6]).is_a_win("o"), True)
        self.assertEqual(Board([1, 4, 7], [3, 6, 9]).is_a_win("o"), True)
        self.assertEqual(Board([1, 9, 6], [3, 5, 7]).is_a_win("o"), True)
        self.assertEqual(Board([1, 3, 6], [7, 8, 9]).is_a_win("o"), True)
        self.assertEqual(Board([2, 9, 6], [3, 4, 7]).is_a_win("o"), False)
        self.assertEqual(Board([2, 3, 6], [4, 5, 9]).is_a_win("o"), False)
        self.assertEqual(Board([2, 9, 6], [5, 2, 3]).is_a_win("o"), False)
        self.assertEqual(Board([1, 9, 6], [3, 5, 8]).is_a_win("o"), False)
        self.assertEqual(Board([1, 9, 6], [7, 5, 6]).is_a_win("o"), False)
        self.assertEqual(Board([1, 4, 7], [8, 6, 9]).is_a_win("o"), False)
        self.assertEqual(Board([1, 9, 6], [2, 5, 7]).is_a_win("o"), False)
        self.assertEqual(Board([1, 3, 6], [5, 8, 9]).is_a_win("o"), False)

    # test to identify if x wins
    def test_x_wins(self):
        self.assertEqual(Board([1, 4, 7], [2, 9, 6]).is_a_win("x"), True)
        self.assertEqual(Board([1, 5, 9], [2, 3, 6]).is_a_win("x"), True)
        self.assertEqual(Board([1, 2, 3], [5, 9, 6]).is_a_win("x"), True)
        self.assertEqual(Board([2, 5, 8], [1, 9, 6]).is_a_win("x"), True)
        self.assertEqual(Board([4, 5, 6], [1, 9, 8]).is_a_win("x"), True)
        self.assertEqual(Board([3, 6, 9], [1, 4, 7]).is_a_win("x"), True)
        self.assertEqual(Board([3, 5, 7], [1, 9, 6]).is_a_win("x"), True)
        self.assertEqual(Board([7, 8, 9], [1, 3, 6]).is_a_win("x"), True)
        self.assertEqual(Board([3, 4, 7], [2, 9, 6]).is_a_win("x"), False)
        self.assertEqual(Board([4, 5, 9], [2, 3, 6]).is_a_win("x"), False)
        self.assertEqual(Board([5, 2, 3], [2, 9, 6]).is_a_win("x"), False)
        self.assertEqual(Board([3, 5, 8], [1, 9, 6]).is_a_win("x"), False)
        self.assertEqual(Board([7, 5, 6], [1, 9, 6]).is_a_win("x"), False)
        self.assertEqual(Board([8, 6, 9], [1, 4, 7]).is_a_win("x"), False)
        self.assertEqual(Board([2, 5, 7], [1, 9, 6]).is_a_win("x"), False)
        self.assertEqual(Board([5, 8, 9], [1, 3, 6]).is_a_win("x"), False)

    # test to check if it'll make middle move as first move
    def test_comp_middle_move(self):
        self.assertEqual(Board([1],[]).computer_move(), 5)
        self.assertEqual(Board([2], []).computer_move(), 5)
        self.assertEqual(Board([3], []).computer_move(), 5)
        self.assertEqual(Board([4], []).computer_move(), 5)
        self.assertNotEqual(Board([5], []).computer_move(), 5)  # if x plays in middle first

    # check if it'll play in last available corner if possible
    def test_corner_move(self):
        self.assertEqual(Board([1, 3, 6], [5, 7]).computer_move(), 9)
        self.assertEqual(Board([9, 3, 6], [5, 7]).computer_move(), 1)
        self.assertEqual(Board([1, 9, 6], [5, 7]).computer_move(), 3)
        self.assertEqual(Board([1, 3, 6], [5, 9]).computer_move(), 7)

    # test if it'll block a wining move



if __name__ == "__main__":
    unittest.main()

