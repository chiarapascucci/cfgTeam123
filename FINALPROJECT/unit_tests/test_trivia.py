from unittest import TestCase, main
from FINALPROJECT.games.trivia_game import TriviaGame


class TestTriviaQuiz(TestCase):

    def test_questions_not_0(self):
        trivia = TriviaGame()
        self.assertTrue(trivia.num_of_questions > 0)

    def test_question_num_not_higher_than_questions(self):
        trivia = TriviaGame()
        self.assertTrue(trivia.num_of_questions > trivia.question_num)

    def test_correct_answer(self):
        trivia = TriviaGame()
        correct_ans = trivia.__next__()['correct_answer']
        result = trivia.check_correct(correct_ans)
        self.assertTrue(result)

    def test_incorrect_answer(self):
        trivia = TriviaGame()
        for incorrect_ans in trivia.__next__()['incorrect_answers']:
            result = trivia.check_correct(incorrect_ans)
            self.assertFalse(result)

    def test_question_iterates(self):
        trivia = TriviaGame()
        count = 0
        num_questions = trivia.num_of_questions
        for question in trivia:
            count += 1
        self.assertEqual(num_questions, count)


if __name__ == '__main__':
    main()
