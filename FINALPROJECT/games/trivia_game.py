from pprint import pprint
import requests

"""output of TriviaGame class is a dictionary of keys (what the user selects) values (options), and correct/incorrect 
answers. e.g.

{'category': 'Entertainment: Books',
 'correct_answer': 'Shadow',
 'difficulty': 'hard',
 'incorrect_answers': ['Thievery', 'Justice', 'Chaos'],
 'question': 'In The Lies Of Locke Lamora, what does &quot;Lamora&quot; mean '
             'in Throne Therin?',
 'type': 'multiple'}

"""


class TriviaGame:
    questions = []
    num_of_questions = 0
    question_num = 0
    current_question = {}

    def __init__(self, num_questions, category, difficulty):
        url = 'https://opentdb.com/api.php?amount={}&category={}&difficulty={}'.format(num_questions, category,
                                                                                       difficulty)
        response = requests.get(url)
        self.questions = response.json()['results']
        self.num_of_questions = num_questions
        self.current_question = self.questions[0]

    def __iter__(self):
        return self

    def __next__(self):
        if self.question_num >= self.num_of_questions:
            raise StopIteration

        result = self.questions[self.question_num]
        self.question_num += 1
        self.current_question = result
        return result

    def get_current_question(self):
        return self.current_question


#
# trivia_game = TriviaGame(10, 9, 'easy')
#
# trivia_game2 = TriviaGame(10, 10, 'hard')

# looping through trivia game instances at the same time (to show 2 games can happen in parallel)
# for question in trivia_game:
#     pprint(question)
#     pprint(trivia_game2.__next__())

