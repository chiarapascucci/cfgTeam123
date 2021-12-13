from pprint import pprint
import random
import requests

"""
Output of TriviaGame class is a dictionary of keys (what the user selects) values (options), and correct/incorrect 
answers.
"""


class TriviaGame:
    questions = []
    num_of_questions = 0
    question_num = 0
    current_question = {}
    num_correct = 0

    # Hard coded trivia options to 10 questions, initialisation of instances
    def __init__(self, num_questions=10, category=None, difficulty=None):
        url = 'https://opentdb.com/api.php?amount={}'.format(num_questions)
        if category:
            url += '&category={}'.format(category)

        if difficulty:
            url += '&difficulty={}'.format(difficulty)

        response = requests.get(url)
        self.questions = response.json()['results']
        self.num_of_questions = num_questions
        self.current_question = self.questions[0]

    def __iter__(self):
        return self

    # Limit to 10 iterations and keep the state of question number
    def __next__(self):
        if self.question_num >= self.num_of_questions:
            raise StopIteration

        result = self.questions[self.question_num]
        self.shuffle_answers(result)
        self.question_num += 1
        self.current_question = result
        return result

    def shuffle_answers(self, result):
        all_answers = [result['correct_answer']]
        all_answers.extend(result['incorrect_answers'])
        random.shuffle(all_answers)
        result['answers'] = all_answers

    # Keep the state of user score
    def check_correct(self, user_answer):
        correct = user_answer == self.current_question['correct_answer']
        if correct:
            self.num_correct += 1
        return correct

    def get_score(self):
        return "{} / {}".format(self.num_correct, self.num_of_questions)








