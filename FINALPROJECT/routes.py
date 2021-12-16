import json
import random
import datetime


from FINALPROJECT.data_access_functions import \
    create_new_session, get_session_id, log_game_record_end_time, update_session_end_time


from FINALPROJECT.forms import RegistrationForm, LoginForm

from FINALPROJECT.games.blackjack import play_game, player_stand, decide_winner, player_hit, \
    jsonify_blackjack_object, recreate_blackjack_object

from FINALPROJECT.games.guess_my_num import play
from FINALPROJECT.games.trivia_game import TriviaGame
from FINALPROJECT.games.ticboard import Board
from FINALPROJECT.data_access_functions import create_new_game_record

from flask import jsonify, request, render_template, url_for, redirect, flash, session
from flask_login import login_user, login_required, logout_user, current_user

from FINALPROJECT import app
from FINALPROJECT.models import CustomAuthUser, get_user_instance

import html


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
        return render_template('select_break_time.html', title='Start the Timer', user_id=user_id)

    if not session.get('username') is None:
        username = session.get('username')
        return render_template('select_break_time.html', title='Start the Timer', username=username)


# need to provide some return type if something goes wrong (i.e. sesssion object does not have user id or username


@app.route('/browsegames')
@login_required
def browsegames():
    return render_template('browsegames.html', title='browsegames')


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    # this is an imported function from the flask_login library which automatically ends the current_users session
    flash('You have been logged out successfully')
    return redirect(url_for('home'))


@app.route('/special')
@login_required
def special():
    if 'username' in session:
        print("user session object contains username: ", session)
    return render_template('special.html', title='special')


################### user registration ###############################

@app.route('/register', methods=['GET', 'POST'])
# as this is a form it's essential that the post method is allowed so that we can send data
def register():
    # registration form is instantiated
    form = RegistrationForm()

    # instantiating the form object from our Registration form class from forms.py
    # this will give us the ability to use the information the user has entered into our form
    # if the form is submitted and it is valid
    # data is extracted to create an instance of user
    if form.validate_on_submit():
        # if the inputs to the form meet the requirements of all the validators we put in place then assign
        # those inputs to the variables below
        username = form.user_name.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        password = form.password.data
        user = CustomAuthUser(user_name=username, first_name=first_name, last_name=last_name, email=email,
                              password=password)
        # created user is saved to the DB
        user.save()

        return redirect(url_for('login'))
    else:
        flash('something went wrong, please try again')
        return render_template('register.html', title='Register', form=form)


#################### user login + authentication ########################

@app.route('/login', methods=['GET', 'POST'])
def login():
    # instantiating the login form
    form = LoginForm()
    # instantiating the object 'form' from the LoginForm class from forms.py to give us the ability to use the information the user has entered into our form
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    # the if statement above is a second level of security to ensure that the user cannot view the log in page if they are already authenticated (logged in)
    # current_user is a proxy which is available in every template, so we can create conditionals depending of if 'current_user' is authenticated in our other html pages
    # if the form is submitted and it is valid
    # data is extracted to log the user in
    if form.validate_on_submit():

        # since the user has provided their user name
        # the username is used to retrieve the relevant user as an instance of User
        user = get_user_instance(user_name=form.user_name.data)
        # password provided is retrieved
        provided_password = form.password.data

        # using method implemented in user class to check if the provided password
        # and the password associated with the instance of user that has been retrieved correspond
        if user.verify_password(pwd=provided_password):
            # if the password is valid
            # the user is logged in
            login_user(user)
            # their user name is saved to the session object
            session['username'] = user.user_name
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
    """
    this function is called when the timer starts by sending an AJAX request to the server
    the request object contains the info needed to create a new session entry in the DB
    :return: returns a JSON obj if creation is successful, None otherwise
    """

    if request.method == 'POST':
        data_dict = request.get_json()
        user_id = data_dict['user_id']
        start_time = data_dict['start_time']
        req_len = str(data_dict['requested_duration'])
        session_id = create_new_session(user_id, start_time, req_len)
        response = {'result': (session_id, user_id), 'redirect_url': url_for('browsegames')}
        result = jsonify(response)

        return result


@app.route('/log-session-end', methods=['GET', 'POST'])
@login_required
def logsessionend():
    """
    This function (similar to the above) is called when the timer expires, by sending an AJAX request.
    The request contains the info needed to update a given session entry with the relevant end time
    :return: returns a JSON object with the data retrieved (as a check) and the url for redirecting the user
    """

    if request.method == 'POST':
        print("post request received")
        print("trying to print json data from request \n", request.get_json())
        print("post request received")
        print("print type of return", type(request.get_json()))
        data_dict = request.get_json()
        user_id = int(data_dict['user_id'])
        end_time = data_dict['end_time']
        session_id = int(data_dict['session_id'])
        result = update_session_end_time(end_time, session_id, user_id)
        response = {'result': result, 'redirect_url': url_for('logout')}
        return jsonify(response)


################################# GAMES RELATED VIEWS ##########################################

#################### TIC TAC TOE #######################

# logs the start of the game in the game record table
@app.route('/tic-tac-toe')
@login_required
def tic_tac_toe():
    if not session.get('_user_id') is None:
        user_id = session.get('_user_id')
        session_id = get_session_id(user_id)
        game_id = create_new_game_record(user_id, 1, session_id)
    return render_template('tic_tac.html', title="tictactoe", game_id=game_id)


@app.route('/tic-tac-ajax', methods=['GET', 'POST'])
def process_tic_tac():
    if request.method == 'POST':
        data = request.get_json()

        # gets the moves and stores in a list
        x_list = [int(c) for c in data['x']]
        o_list = [int(c) for c in data['o']]
        print(x_list)
        print(o_list)

        board1 = Board(x_list, o_list)

        comp_move = board1.computer_move()
        computer_win = board1.is_a_win(board1.board, "o")
        human_win = board1.is_a_win(board1.board, "x")

        # creating a json that can be used by ajax
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
    game_record = int(game_state)
    print("SESSION ENDED AND LOGGED TO PYTHON")
    log_game_record_end_time(game_record)
    return "Session Ended"


################# BLACKJACK ####################

@app.route('/blackjack')
@login_required
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
    return render_template('trivia-quiz.html', title='Trivia Quiz', question=html.unescape(first_q['question']),
                           answers=answers, len=len(answers),
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
# logs the start of the game in the game record table
@app.route('/guess-my-number')
@login_required
def guess_my_num_game():
    comp_num = random.randint(1, 200)
    if not session.get('_user_id') is None:
        user_id = session.get('_user_id')
        session_id = get_session_id(user_id)
        game_id = create_new_game_record(user_id, 4, session_id)
    return render_template('guess_number.html', title="guess_my_number", number=comp_num, game_id=game_id)


# this function process the ajax request coming from the client
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
    game_record = int(game_state)
    print("SESSION ENDED AND LOGGED TO PYTHON")
    log_game_record_end_time(game_record)
    return "Session Ended"


############### USER ANALYTICS ##################
# retrieves and displays the user game history
@app.route('/user_analytics')
@login_required
def user_analytics():
    if not session.get('_user_id') is None:
        user_id = session.get('_user_id')
        game_history = display_total_game_history(user_id)
        game_history = display_game_history(game_history)
    return render_template('user_analytics.html', title="user_analytics", game_history=game_history)


def display_game_history(game_history):
    simplified_history = []
    for item in game_history:
        game = item[0]
        date = item[2].date()
        game_time = item[3] - item[2]
        record = [game, date, game_time]
        simplified_history.append(record)
    return simplified_history
