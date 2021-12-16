import json
"""
    this is a very simple implementation of a tic tac toe game
    the game does not run end-to-end within this file
    rather this implementation provides a function that can take a representation of a tic tac toe board
    and return an object (python dictionary) representing the next step in the game
"""

"""
    for simplicity a board is thought of being made up of 9 numbered cells (1-9) which are in a fixed position like so:
    
             |     |     
          1  |  2  |  3  
        _____|_____|_____
             |     |     
          4  |  5  |  6  
        _____|_____|_____
             |     |     
          7  |  8  |  9  
             |     |  

    The game can be implemented in different ways (functionally or with class-based design). But the main requirement for 
    it to work with the current front-end is to have a function that can take a representation of the above board in any state (e.g. 
    empty or with some o and x already on it), analyse it, and return the correct next step

"""

"""
    By way of an example, here is how the below code implements the game with the front end:
    
    - User starts the game with an empty board
    - User clicks on a cell where they wish to place a X
    - Ajax magic capture a snapshot of this: they capture the board as at that moment (empty) + user desired move (say user
      wants to play on cell no. 7)
    - Middleware function (in routes.py) receives this data (packaged inside an ajax request) and unpacks it and re-packs it
      in a way that the function below can handle it
    - the chosen format for the data going to the function is a python dictionary containing two lists of integers, representing 
      the cell numbers, one list is assigned to x and to o. So for this example the dictionary would look like this:
            state = { 'x': [7], 'o':[] }
            the player has clicked on cell 7 so number 7 has been added to the list of "x_cells"/"human_cells", while the o list
            ("computer_cells") is still empty, because the computer is yet to make a move
    - once we know how the data is getting to the function, we can interpret it and have the computer work out its move 
      accordingly
    - the important last step is for the function to return data back. This can be structured in many ways, below I have
      chosen a dictionary object (for ease) with this structure: {'comp_move': <int representing the cell where the computer
      wants to play, empty if no next move>, 'comp_win': T/F, 'human_win': T/F, 'end_game':T/F}
"""


def receive_move(state):
    cells = {1, 2, 3, 4, 5, 6, 7, 8, 9}

    human_cells = state['x']
    comp_cells = state['o']

    hooman_win = check_if_win(state)
    if not hooman_win:
        cells.difference_update(human_cells, comp_cells)
        if cells:
            chosen_cell = cells.pop()
            state['o'].add(chosen_cell)
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
