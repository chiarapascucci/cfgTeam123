from unittest import TestCase, main

from FINALPROJECT.games.guess_my_num import play


class TestNumberGame(TestCase):
    def test_human_win_logic(self):
        h_guess = 10
        c_num = 10
        guess_no = 3
        expected_output = True
        actual_output = play(h_guess, c_num, guess_no)
        self.assertEqual(expected_output, actual_output['human_win'])

    def test_human_win_msg(self):
        h_guess = 100
        c_num = 100
        guess_no = 3
        expected_output = 'you win'
        actual_output = play(h_guess, c_num, guess_no)
        self.assertEqual(expected_output, actual_output['msg'])

    def test_no_win_logic(self):
        h_guess = 150
        c_num = 100
        guess_no = 7
        expected_output = False
        actual_output = play(h_guess, c_num, guess_no)
        self.assertEqual(expected_output, actual_output['human_win'])

    def test_game_end_logic(self):
        h_guess = 150
        c_num = 100
        guess_no = 9
        expected_output = True
        actual_output = play(h_guess, c_num, guess_no)
        self.assertEqual(expected_output, actual_output['game_end'])

    def game_end_msg(self):
        h_guess = 150
        c_num = 100
        guess_no = 9
        expected_output = 'you run out of guesses'
        actual_output = play(h_guess, c_num, guess_no)
        self.assertEqual(expected_output, actual_output['msg'])

    def test_too_high(self):
        h_guess = 150
        c_num = 100
        guess_no = 4
        expected_output = 'too high'
        actual_output = play(h_guess, c_num, guess_no)
        self.assertEqual(expected_output, actual_output['msg'])

    def test_too_low(self):
        h_guess = 10
        c_num = 150
        guess_no = 4
        expected_output = 'too low'
        actual_output = play(h_guess, c_num, guess_no)
        self.assertEqual(expected_output, actual_output['msg'])

    def test_number_guesses(self):
        h_guess = 10
        c_num = 150
        guess_no = 4
        expected_output = guess_no+1
        actual_output = play(h_guess, c_num, guess_no)
        self.assertEqual(expected_output, actual_output['guess_no'])

if __name__ == '__main__':
    main()