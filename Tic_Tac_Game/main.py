from ticplayer import Player
from ticboard import Board


def start_game():
    print("WELCOME!\n")
    board1 = Board()
    board1.display_board()
    return board1


def pick_letter():
    person1 = Player(name="Jane", computer_player=False)
    computer1 = Player()

    flag = True
    while flag:
        try:
            is_x_or_o = input("X goes first, \nWould you like to be \"X\" or \"O\": ")
            is_x_or_o = is_x_or_o.upper()

            if is_x_or_o == "X" or is_x_or_o == "O":
                if is_x_or_o == "O":
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


def human_turn(board1, person1):
    person1.human_move()
    board1.display_board()


def computer_turn(board1, computer1):
    move = computer1.computer_move()
    if move == 0:
        a_draw(board1)
    else:
        board1.make_move(computer1.letter, move)
        print(f"Computer placed {computer1.letter} in position {move}: ")
        board1.display_board()


def human_play_first(person1, computer1, board1):
    # While there is space to play
    while not(board1.no_space_on_board()):
        # if the winner is not computer then you play next
        if not (board1.is_a_win(Board.board_board(), computer1.letter)):
            human_turn(board1, person1)
        else:
            print("You lose, O won")
            break

        if not (board1.is_a_win(Board.board_board(), person1.letter)):
            computer_turn(board1, computer1)

        else:
            print("You WIN!, Congratulations")
            break

    a_draw(board1)


def computer_play_first(board1, person1, computer1):

    # While there is space to play
    while not(board1.no_space_on_board()):
        if not (board1.is_a_win(Board.board_board(), person1.letter)):
            computer_turn(board1, computer1)
        else:
            print("You WIN!, Congratulations")
            break

        # if the winner is not computer then you play next
        if not (board1.is_a_win(Board.board_board(), computer1.letter)):
            human_turn(board1, person1)
        else:
            print("You lose, O won")
            break

    a_draw(board1)


# if no more spaces to make a move then  no winner yet it's a tie
def a_draw(board1):
    if board1.no_space_on_board():
        print("It's a Draw!")


# "X" goes first
def tic_tac_play():
    board1 = start_game()
    game = pick_letter()
    (person1, computer1) = game

    if person1.letter == "X":
        human_play_first(person1, computer1, board1)
    else:
        computer_play_first(board1, person1, computer1)


if __name__ == '__main__':
    tic_tac_play()

