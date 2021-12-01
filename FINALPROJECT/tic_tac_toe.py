import json


def receive_move(state):
    cells = {1, 2, 3, 4, 5, 6, 7, 8, 9}
    print(state)

    human_cells = state['x']
    comp_cells = state['o']

    hooman_win = check_if_win(state)
    print("checking if anyone wins with current board state: ", hooman_win)
    if not hooman_win:
        cells.difference_update(human_cells, comp_cells)
        if cells:
            print(cells)
            chosen_cell = cells.pop()
            print(chosen_cell)
            state['o'].add(chosen_cell)
            print(state)
            comp_win = check_if_win(state)
            if not comp_win:
                return {'comp_move': str(chosen_cell), 'comp_win': '1', 'hum_win': '1', 'game_end': '1'}
            else:
                return {'comp_move': str(chosen_cell), 'comp_win': '0', 'hum_win': '1', 'game_end': '1'}
        else:
            return {'comp_move': '', 'comp_win': '1', 'hum_win': '1', 'game_end': '0'}
    else:
        return {'comp_move': '', 'comp_win': '1', 'hum_win': '0', 'game_end': '1'}


def check_if_win(state: dict):
    winning_sets = [
        {1, 2, 3},
        {4, 5, 6},
        {7, 8, 9},
        {1, 4, 7},
        {2, 5, 8},
        {3, 6, 9},
        {1, 5, 9},
        {3, 5, 7},
    ]
    for combo in winning_sets:
        print(f"combo {combo} is a subset of o cells : {state['o']} ?  ", combo.issubset(state['o']))
        if combo.issubset(state['x']) or combo.issubset(state['o']):
            return True

    return False


# for testing
if __name__ == '__main__':
    state = {
        'x': ['1', '4'],
        'o': ['5', '8', '2']
    }

    result = receive_move(state)
    print(result)
