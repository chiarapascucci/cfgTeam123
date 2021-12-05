import random

from FINALPROJECT import app
from FINALPROJECT.games.trivia_game import TriviaGame
from flask import Flask, jsonify, request, render_template, url_for, redirect, flash
from FINALPROJECT.data_access_functions import create_new_game_record


trivia_games = {}


@app.route('/trivia-quiz')
def trivia_quiz():
    game_id = create_trivia().json
    print(game_id)
    first_q = next_question(game_id).json
    print(first_q)
    answers = [first_q['correct_answer']]
    answers.extend(first_q['incorrect_answers'])
    random.shuffle(answers)
    return render_template('trivia-quiz.html', title='Trivia Quiz', question=first_q['question'], answers=answers, len=len(answers),
                           game_id=game_id, q_num=1)


@app.route('/trivia-quiz/create')
def create_trivia():
    user_id = 5 # replace with real user_id
    session_id = 1 # replace wth real session_id
    # call data access layer function to create game record
    game_id = create_new_game_record(user_id, 3, session_id)
    print(game_id)
    trivia_game = TriviaGame()
    trivia_games[game_id] = trivia_game
    return jsonify(game_id)


@app.route('/trivia-quiz/<game_id>/next-question')
def next_question(game_id):
    game_id = int(game_id)
    next_q = trivia_games[game_id].__next__()
    return jsonify(next_q)


@app.route('/trivia-quiz/<game_id>/check-answer/<user_answer>')
def check_question(game_id, user_answer):
    game_id = int(game_id)
    current_q = trivia_games[game_id].get_current_question()
    if current_q['correct_answer'] == user_answer:
        return jsonify("Correct! :)")
    return jsonify("Incorrect :(")







