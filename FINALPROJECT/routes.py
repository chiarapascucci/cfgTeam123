import json
import random

from FINALPROJECT.data_access_functions import create_user_in_db, DBConnectionError, _connect_to_db, \
    create_new_session, get_session_id, log_game_record_end_time

from FINALPROJECT.games.blackjack import play_game, player_hit_or_stand, player_stand, decide_winner, player_hit

from FINALPROJECT.forms import RegistrationForm, LoginForm

from FINALPROJECT.games.blackjack import play_game, player_stand, decide_winner, player_hit, \
    jsonify_blackjack_object, recreate_blackjack_object

from FINALPROJECT.games.guess_my_num import play
from FINALPROJECT.games.trivia_game import TriviaGame
from FINALPROJECT.games.Tic_Tac_Game.ticboard import Board
from FINALPROJECT.data_access_functions import create_new_game_record

from flask import jsonify, request, render_template, url_for, redirect, flash, session
from flask_login import login_user, login_required, logout_user, current_user

from FINALPROJECT import app
from FINALPROJECT.models import UserNotFoundException, CustomAuthUser, fetch_user_info_with_username, get_user_instance
from FINALPROJECT.config import DB_NAME

import html

###### this file is a bit of a mess lol ########

########### basic routes ############


@app.route('/')
def home():
    return render_template('home.html', title='home')


@app.route('/start-timer')
@login_required
def starttimer():
    print(session)
    if not session.get('_user_id') is None:
        user_id = session.get('_user_id')
        print(user_id)
        print(type(user_id))

    if not session.get('username') is None:
        username = session.get('username')
    return render_template('select_break_time.html', title='Start the Timer', user_id=user_id)


@app.route('/browsegames')
def browsegames():
    return render_template('browsegames.html', title='browsegames')


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash('You have been logged out successfully')
    return redirect(url_for('home'))


@app.route('/special')
@login_required
def special():
    if 'username' in session:
        print("user session object contains username: ", session)
    return render_template('special.html', title='special')


############# user registration ################

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.user_name.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        password = form.password.data

        print(type(password))
        user = CustomAuthUser(user_name=username, first_name=first_name, last_name=last_name, email=email,
                              password=password)
        user.save()
        outcome = True
        if outcome:
            flash(f'Account created for {form.user_name.data}!', 'Success')
            return redirect(url_for('login'))
        else:
            flash('something went wrong, please try again')
            return render_template('register.html', title='Register', form=form)
    return render_template('register.html', title='Register', form=form)


#################### user login + authentication ########################


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if current_user.is_authenticated:
        return redirect(url_for('home'))

    if form.validate_on_submit():
        print(form.user_name.data)
        user = get_user_instance(user_name=form.user_name.data)
        provided_password = form.password.data
        print(type(provided_password))
        print(provided_password)
        if user.verify_password(pwd=provided_password):
            login_user(user)
            session['username'] = user.user_name
            session['used_id'] = user.id
            flash('You have been logged in', 'success')
            return redirect(url_for('starttimer'))
        else:
            flash('details provided are not correct, please try again')
            return render_template('login.html', title='login', form=form)

    return render_template('login.html', title='login', form=form)


############## TIMER RELATED views ######################

@app.route('/log-session-start', methods=['GET', 'POST'])
@login_required
def logsessionstart():
    """will need some way of retrieving user ID"""
    try:
        connection = _connect_to_db()
        if request.method == 'POST':
            print("post request received")

            data_dict = request.get_json()
            user_id = data_dict['user_id']
            start_time = data_dict['start_time']
            req_len = str(data_dict['requested_duration'])
            print(data_dict)
            session_created = create_new_session(user_id, start_time, req_len)
            follow_query = f"select * from {DB_NAME}.sessions WHERE UserID = {user_id} ORDER BY SessionID DESC LIMIT 1;"
            print(follow_query)
            other_cur = connection.cursor()
            other_cur.execute(follow_query)
            result = other_cur.fetchall()
            response = {'result': result, 'redirect_url': url_for('browsegames')}
            print("printing result of query to get latest entry: ", result)
            result = jsonify(response)

            other_cur.close()
            connection.close()
            print("connection closed")
            return result

    except DBConnectionError:
        print("db connection failed")


@app.route('/log-session-end', methods=['GET', 'POST'])
@login_required
def logsessionend():
    try:
        connection = _connect_to_db()
        if request.method == 'POST':
            print("post request received")
            print("trying to print json data from request \n", request.get_json())
            print("post request received")
            print("print type of return", type(request.get_json()))
            data_dict = request.get_json()
            user_id = int(data_dict['user_id'])
            end_time = data_dict['end_time']
            session_id = int(data_dict['session_id'])
            query = f"UPDATE {DB_NAME}.sessions SET EndTime = '{end_time}' WHERE SessionID = {session_id} AND UserID = {user_id};"
            print(query)
            my_cur = connection.cursor()
            my_cur.execute(query)
            result = my_cur.fetchall()
            connection.commit()
            check_query = f"SELECT * FROM {DB_NAME}.sessions WHERE SessionID = {session_id};"
            print("printin check query ", check_query)
            my_cur.execute(check_query)
            check_result = my_cur.fetchall()
            print("printing check result: ", check_result)
            my_cur.close()
            connection.close()
            response = {'result': result, 'redirect_url': url_for('browsegames')}
            print("connection closed")
            return jsonify(response)

    except DBConnectionError:
        print("db connection failed")


################################# GAMES RELATED VIEWS ##########################################

#################### TIC TAC TOE #######################

@app.route('/tic-tac-toe')
@login_required
def tic_tac_toe():
    return render_template('tic_tac.html', title="tictactoe")


# logs the start of the game in the game record table
@app.route('/tic-tac-game-record', methods=['GET', 'POST'])
def log_game_record():
    if not session.get('_user_id') is None:
        user_id = session.get('_user_id')
        session_id = get_session_id(user_id)
        game_record = create_new_game_record(user_id, 1, session_id)
        game_state = {'game_record': str(game_record)}
    return jsonify(game_state)


@app.route('/tic-tac-ajax', methods=['GET', 'POST'])
def process_tic_tac():
    if request.method == 'POST':
        data = request.get_json()
        print(data)
        # state = {}
        x_list = [int(c) for c in data['x']]
        o_list = [int(c) for c in data['o']]
        print(x_list)
        print(o_list)

        board1 = Board(x_list, o_list)

        comp_move = board1.computer_move()
        computer_win = board1.is_a_win("o")
        human_win = board1.is_a_win("x")

        if computer_win:
            return jsonify({'comp_move': comp_move, 'comp_win': True, 'hum_win': False, 'game_end': False})

        elif human_win:
            return jsonify({'comp_move': -1, 'comp_win': False, 'hum_win': True, 'game_end': False})
        elif comp_move == -1:
            return jsonify({'comp_move': -1, 'comp_win': False, 'hum_win': False, 'game_end': True})
        else:
            return jsonify({'comp_move': comp_move, 'comp_win': False, 'hum_win': False, 'game_end': False})


@app.route('/tic-tac-end', methods=['GET', 'POST'])
def tic_tac_end():
    game_state = request.get_json()
    game_record = int(json.loads(game_state['game_record']))
    print("SESSION ENDED AND LOGGED TO PYTHON")
    log_game_record_end_time(game_record)
    return "Session Ended"


################# BLACKJACK ####################

@app.route('/blackjack')
def blackjack():
    return render_template('blackjack.html', title='Blackjack')


# logs the start of the game in the game record table
@app.route('/blackjack-game-record', methods=['GET', 'POST'])
def log_blackjack_game_record():
    if not session.get('_user_id') is None:
        user_id = session.get('_user_id')
        session_id = get_session_id(user_id)
        game_record = create_new_game_record(user_id, 2, session_id)
        game_state = {'game_record': str(game_record)}
    return jsonify(game_state)


# start game, instantiate new blackjack object and deal cards to player and dealer
@app.route('/blackjack-start', methods=['GET', 'POST'])
def start_blackjack_game():
    game_state = request.get_json()
    game_record = game_state['game_record']
    blackjack_object, blackjack_cards, is_blackjack_true, value_of_starting_hands = play_game()
    players_cards = json.dumps((blackjack_cards[0][0].card, blackjack_cards[0][1].card))
    dealers_cards = json.dumps((blackjack_cards[1][0].card, blackjack_cards[1][1].card))
    remaining_cards_in_deck = json.dumps(blackjack_object.blackjack_deck.cards)
    game_state = {'players_cards': players_cards,
                  'dealers_cards': dealers_cards,
                  'cards_in_deck': remaining_cards_in_deck,
                  'is_blackjack_true': is_blackjack_true,
                  'value_of_starting_hands': value_of_starting_hands,
                  'game_record': game_record}
    return jsonify(game_state)


# calculate winner when player stands
@app.route('/blackjack-player-stand', methods=['GET', 'POST'])
def player_stand_blackjack():
    game_state = request.get_json()
    game_record = game_state['game_record']
    blackjack_cards, blackjack_object = recreate_blackjack_object(game_state)
    blackjack_cards = player_stand(blackjack_object, blackjack_cards)
    cards_in_deck, dealers_cards, players_cards = jsonify_blackjack_object(blackjack_cards, blackjack_object)
    value_of_hand = blackjack_object.display_value_of_hands(blackjack_cards)
    winner = decide_winner(blackjack_object, blackjack_cards)
    game_state = {'players_cards': players_cards,
                  'dealers_cards': dealers_cards,
                  'cards_in_deck': cards_in_deck,
                  'value_of_starting_hands': value_of_hand,
                  'winner': winner,
                  'game_record': game_record}
    return jsonify(game_state)


# deal another card to player, calculate if player goes "bust"
@app.route('/blackjack-player-hit', methods=['GET', 'POST'])
def player_hit_blackjack():
    game_state = request.get_json()
    game_record = game_state['game_record']
    blackjack_cards, blackjack_object = recreate_blackjack_object(game_state)
    blackjack_cards = player_hit(blackjack_object, blackjack_cards)
    cards_in_deck, dealers_cards, players_cards = jsonify_blackjack_object(blackjack_cards, blackjack_object)
    if blackjack_object.calculate_value_of_hand(blackjack_cards[0]) <= 21:
        value_of_hand = blackjack_object.display_value_of_players_hand(blackjack_cards)
        winner = 'None'
        game_state = {'players_cards': players_cards,
                      'dealers_cards': dealers_cards,
                      'cards_in_deck': cards_in_deck,
                      'value_of_starting_hands': value_of_hand,
                      'winner': winner,
                      'game_record': game_record}
        return jsonify(game_state)
    else:
        value_of_hand = blackjack_object.display_value_of_hands(blackjack_cards)
        winner = False
        game_state = {'players_cards': players_cards,
                      'dealers_cards': dealers_cards,
                      'cards_in_deck': cards_in_deck,
                      'value_of_starting_hands': value_of_hand,
                      'winner': winner,
                      'game_record': game_record}
        return jsonify(game_state)


@app.route('/blackjack-end', methods=['GET', 'POST'])
def blackjack_end():
    game_state = request.get_json()
    game_record = int(json.loads(game_state['game_record']))
    print("SESSION ENDED AND LOGGED TO PYTHON")
    log_game_record_end_time(game_record)
    return "Session Ended"



################ TRIVIA #########################
trivia_games = {}


# Initiate trivia game
@app.route('/trivia-quiz')
@login_required
def trivia_quiz():
    user_id = session.get('_user_id')
    game_id = create_trivia(user_id)
    first_q = next_question(game_id).json['next_question']
    answers = first_q['answers']
    for index, answer in enumerate(answers):
        answers[index] = html.unescape(answer)
    return render_template('trivia-quiz.html', title='Trivia Quiz', question=html.unescape(first_q['question']), answers=answers, len=len(answers),
                           game_id=game_id, q_num=1)


# Create an instance of a trivia game, make a mapping between game_id and the created instance
def create_trivia(user_id):
    session_id = get_session_id(user_id)
    # call data access layer function to create game record
    game_id = create_new_game_record(user_id, 3, session_id)
    trivia_game = TriviaGame()
    trivia_games[game_id] = trivia_game
    return game_id


# Make a call to next() function to get next question
@app.route('/trivia-quiz/<game_id>/next-question')
def next_question(game_id):
    game_id = int(game_id)
    trivia_game = trivia_games[game_id]
    try:
        next_q = next(trivia_game)
    except StopIteration:
        next_q = None
    return jsonify({"question_num": trivia_game.question_num,
                    "score": trivia_game.get_score(),
                    "next_question": next_q})


# Check user answer with correct/incorrect answers
@app.route('/trivia-quiz/<game_id>/check-answer', methods=['POST'])
def check_question(game_id):
    data = request.get_json()
    game_id = int(game_id)
    correct = trivia_games[game_id].check_correct(data['user_answer'])
    if correct:
        return jsonify("Correct! :)")
    return jsonify("Incorrect :(")


@app.route('/trivia-end', methods=['GET', 'POST'])
def trivia_end():
    game_state = request.get_json()
    game_record = int(game_state)
    print("SESSION ENDED AND LOGGED TO PYTHON")
    log_game_record_end_time(game_record)
    return "Session Ended"


############### GUESS MY NUMBER ##################
@app.route('/guess-my-number')
@login_required
def guess_my_num_game():
    comp_num = random.randint(1, 200)
    print(comp_num)
    return render_template('guess_number.html', title="guess_my_number", number=comp_num)


# logs the start of the game in the game record table
@app.route('/guess-num-game-record', methods=['GET', 'POST'])
def log_guess_number_game_record():
    if not session.get('_user_id') is None:
        user_id = session.get('_user_id')
        session_id = get_session_id(user_id)
        game_record = create_new_game_record(user_id, 4, session_id)
        game_state = {'game_record': str(game_record)}
    return jsonify(game_state)


@app.route('/number-ajax', methods=['GET', 'POST'])
def guess_my_num_game_process():
    if request.method == 'POST':
        data = request.get_json()
        print(data)

        comp_num = int(data['comp_num'])
        human_num = int(data['human_num'])
        guess_num = int(data['no_of_guesses'])

        result = play(human_guess=human_num, computer_num=comp_num, num_of_guesses=guess_num)
        print(result)
        return jsonify(result)


@app.route('/guess-num-end', methods=['GET', 'POST'])
def guess_num_end():
    game_state = request.get_json()
    game_record = int(json.loads(game_state['game_record']))
    print("SESSION ENDED AND LOGGED TO PYTHON")
    log_game_record_end_time(game_record)
    return "Session Ended"
