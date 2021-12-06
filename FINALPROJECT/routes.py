import json

from FINALPROJECT import app
from FINALPROJECT.data_access_functions import create_user_in_db, validate_user, DBConnectionError, _connect_to_db, \
    create_new_session
from FINALPROJECT.forms import RegistrationForm, LoginForm
from flask import jsonify, request, render_template, url_for, redirect, flash

from FINALPROJECT.config import DB_NAME
from FINALPROJECT.games.tic_tac_toe import receive_move
from FINALPROJECT.games.blackjack import play_game, player_hit_or_stand, player_hit, player_stand, decide_winner

"""
https://hackersandslackers.com/configure-flask-applications/
above is link with info about app.config for when you want / encrypt information i think
"""


@app.route('/')
def home():
    return render_template('home.html', title='home')


# @app.route('/tester')
# def tester():
#     return render_template('tester.html', title='tester')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # hashed_pass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        create_user_in_db(form.user_name.data, form.first_name.data, form.last_name.data, form.password.data)
        flash(f'Account created for {form.user_name.data}!', 'Success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        validate_user(form.user_name.data, form.password.data)
        flash('You have been logged in', 'success')
        return redirect(url_for('home'))
    else:
        flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='login', form=form)


@app.route('/tic-tac-toe')
def tic_tac():
    return render_template('tic_tac.html', title='Tic Tac Toe!')


@app.route('/tic-tac-toe-ajax')
def process_tic_tac_toe():
    pass


@app.route('/start-timer')
def starttimer():
    return render_template('select_break_time.html', title='Start the Timer')


@app.route('/browsegames')
def browsegames():
    return render_template('browsegames.html', title='browsegames')


@app.route('/log-session-start', methods=['GET', 'POST'])
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
            session_created = create_new_session(user_id, start_time, req_len)
            follow_query = f"select * from {DB_NAME}.sessions WHERE UserID = {user_id} ORDER BY SessionID DESC LIMIT 1;"
            print(follow_query)
            other_cur = connection.cursor()
            other_cur.execute(follow_query)
            result = other_cur.fetchall()
            print("printing result of query to get latest entry: ", result)
            result = jsonify(result)

            other_cur.close()
            connection.close()
            print("connection closed")
            return result

    except DBConnectionError:
        print("db connection failed")


@app.route('/log-session-end', methods=['GET', 'POST'])
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
            print("connection closed")
            return jsonify(result)

    except DBConnectionError:
        print("db connection failed")


@app.route('/play-tic-tac-toe')
def tic_tac_toe():
    return render_template('tic_tac.html', title="tictactoe")


@app.route('/tic-tac-ajax', methods=['GET', 'POST'])
def process_tic_tac():
    if request.method == 'POST':

        data = request.get_json()

        print(data)
        state = {}
        x_list = [int(c) for c in data['x']]
        o_list = [int(c) for c in data['o']]
        print(x_list)
        print(o_list)

        state['x'] = set(x_list)
        state['o'] = set(o_list)

        result = receive_move(state)
        return jsonify(result)


@app.route('/blackjack')
def blackjack():
    return render_template('blackjack.html', title='Blackjack')


# start game, instantiate new blackjack object and deal cards to player and dealer
@app.route('/blackjack-start', methods=['GET'])
def start_blackjack_game():
    blackjack_object, blackjack_cards, is_blackjack_true, value_of_starting_hands = play_game()
    players_cards = json.dumps((blackjack_cards[0][0].card, blackjack_cards[0][1].card))
    dealers_cards = json.dumps((blackjack_cards[1][0].card, blackjack_cards[1][1].card))
    remaining_cards_in_deck = json.dumps(blackjack_object.blackjack_deck.cards)
    game_state = {'players_cards': players_cards,
                  'dealers_cards': dealers_cards,
                  'cards_in_deck': remaining_cards_in_deck,
                  'is_blackjack_true': is_blackjack_true,
                  'value_of_starting_hands': value_of_starting_hands}
    return jsonify(game_state)


# calculate winner when player stands
@app.route('/blackjack-player-stand', methods=['GET', 'POST'])
def player_stand_blackjack():
    game_state = request.get_json()
    players_cards = json.loads(game_state['players_cards'])
    dealers_cards = json.loads(game_state['dealers_cards'])
    cards_in_deck = json.loads(game_state['cards_in_deck'])
    blackjack_object, blackjack_cards = player_hit_or_stand(players_cards, dealers_cards, cards_in_deck)
    blackjack_cards = player_stand(blackjack_object, blackjack_cards)
    players_cards = blackjack_cards[0]
    dealers_cards = blackjack_cards[1]
    players_cards = json.dumps([players_card.card for players_card in players_cards])
    dealers_cards = json.dumps([dealers_card.card for dealers_card in dealers_cards])
    cards_in_deck = json.dumps(blackjack_object.blackjack_deck.cards)
    value_of_hand = blackjack_object.display_value_of_hands(blackjack_cards)
    winner = decide_winner(blackjack_object, blackjack_cards)
    game_state = {'players_cards': players_cards,
                  'dealers_cards': dealers_cards,
                  'cards_in_deck': cards_in_deck,
                  'value_of_starting_hands': value_of_hand,
                  'winner': winner}
    return jsonify(game_state)


# deal another card to player, calculate if player goes "bust"
@app.route('/blackjack-player-hit', methods=['GET', 'POST'])
def player_hit_blackjack():
    game_state = request.get_json()
    players_cards = json.loads(game_state['players_cards'])
    dealers_cards = json.loads(game_state['dealers_cards'])
    cards_in_deck = json.loads(game_state['cards_in_deck'])
    blackjack_object, blackjack_cards = player_hit_or_stand(players_cards, dealers_cards, cards_in_deck)
    blackjack_cards = player_hit(blackjack_object, blackjack_cards)
    players_cards = blackjack_cards[0]
    dealers_cards = blackjack_cards[1]
    players_cards = json.dumps([players_card.card for players_card in players_cards])
    dealers_cards = json.dumps([dealers_card.card for dealers_card in dealers_cards])
    cards_in_deck = json.dumps(blackjack_object.blackjack_deck.cards)
    if blackjack_object.calculate_value_of_hand(blackjack_cards[0]) <= 21:
        value_of_hand = blackjack_object.display_value_of_players_hand(blackjack_cards)
        winner = 'None'
        game_state = {'players_cards': players_cards,
                      'dealers_cards': dealers_cards,
                      'cards_in_deck': cards_in_deck,
                      'value_of_starting_hands': value_of_hand,
                      'winner': winner}
        return jsonify(game_state)
    else:
        value_of_hand = blackjack_object.display_value_of_hands(blackjack_cards)
        winner = False
        game_state = {'players_cards': players_cards,
                      'dealers_cards': dealers_cards,
                      'cards_in_deck': cards_in_deck,
                      'value_of_starting_hands': value_of_hand,
                      'winner': winner}
        return jsonify(game_state)
