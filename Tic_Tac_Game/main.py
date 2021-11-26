import ticboard
from ticplayer import Player
from ticboard import Board


def intro_game():
    print("WELCOME!\n")
    board1 = Board()
    board1.display_board()
    return board1


def create_game():
    person1 = Player(name="Jane", computer_player=False)
    computer1 = Player()

    flag = True
    while flag:
        try:
            go_first = input("\nWould you like to be \"X\" or \"O\": ")
            go_first = go_first.upper()

            """# try not in () if this works """
            if go_first == "X" or go_first == "O":
                if go_first == "O":
                    person1.letter = "O"
                    flag = False
                else:
                    computer1.letter = "O"
                    flag = False
            else:
                print("Please enter \"X\" or \"O\"")

        except ValueError:
            print("No numbers please, just \"X\" or \"O\"")

    return person1, computer1


def tic_tac_play():
    # unpacks create_game()
    board1 = intro_game()
    game = create_game()
    (person1, computer1) = game


    # While there is space to play
    while not(board1.no_space_on_board()):
        # if the winner is not O (computer) then you play next
        # Always checking for winner
        if not(board1.is_a_win(Board.board_board(), computer1.letter)):
            person1.human_move()
            board1.display_board()
        else:
            print("You lose, O won")
            break

        # Check to see if player(X) won
        if not(board1.is_a_win(Board.board_board(), person1.letter)):
            move = computer1.computer_move()
            if move == 0:
                print("It's a tie")
            else:
                board1.make_move(computer1.letter, move)
                print(f"Computer placed \"O\" in position {move}: ")
                board1.display_board()

        else:
            print("You WIN!, Congratulations")
            break

    # if there are no more spaces to make a move
    # there was no winner to it's a tie
    if board1.no_space_on_board():
        print("It's a Draw")



if __name__ == '__main__':
    tic_tac_play()

