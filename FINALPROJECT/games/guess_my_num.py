

def play(human_guess:int, computer_num:int, num_of_guesses:int):
    num_of_guesses += 1
    if human_guess == computer_num:
        return {'human_win': True, 'comp_num': computer_num,
                'guess_no': num_of_guesses, 'game_end': False, 'msg': "you win"}
    else:
        if num_of_guesses >= 10:
            return {'human_win': False, 'comp_num': computer_num,
                    'guess_no': num_of_guesses, 'game_end': True, 'msg': "you run out of guesses"}
        else:
            if human_guess > computer_num:
                return {'human_win': False, 'comp_num': computer_num,
                        'guess_no': num_of_guesses, 'game_end': False, 'msg': "too high"}
            else:
                return {'human_win': False, 'comp_num': computer_num,
                        'guess_no': num_of_guesses, 'game_end': False, 'msg': "too low"}

