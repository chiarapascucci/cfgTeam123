# THE GOAL IS TO GET TO AS CLOSE TO 21 BUT NOT ABOVE 21
# IF YOU GET 21 WITH YOUR FIRST TWO CARDS THAT IS BLACKJACK
# AN ACE CAN BE EITHER HIGH OR LOW [1 OR 11]
# Two cards are dealt to the player facing upwards (visible to everyone).
# The dealer deals himself two cards one visible to everyone, and one facing downwards.
# The player has to decide whether to stand with the current set of cards or get another card.
# If the player decides to hit, another card is dealt to the player.
# When the player decides to stand, then the dealer reveals his hidden card/s.
# The dealer does not have the authority to decide whether to hit or stand.
# The general rule is that the dealer needs to keep hitting more cards if the sum of dealer’s cards is less than 17.
# As soon as the sum of dealer’s cards is either 17 or more, the dealer is obliged to stand.
# According to the final sum of the cards, the winner is decided.

from random import randint
from math import floor


def main():
    print('Welcome to Blackjack')
    start_game = input('Would you like to play? [Y / N]\n')
    if start_game.upper() == "Y":
        blackjack, blackjack_cards, is_blackjack_true = play_game()
        if not is_blackjack_true:
            hit_or_stand(blackjack, blackjack_cards)
        else:
            print('You Won!\n Goodbye')
    else:
        print('Goodbye')


def play_game():
    blackjack = Blackjack()
    blackjack.shuffle()
    blackjack_cards = blackjack.begin_game()
    is_blackjack_true = blackjack.is_blackjack(blackjack_cards)
    return blackjack, blackjack_cards, is_blackjack_true


def hit_or_stand(blackjack, blackjack_cards):
    hit = input('Would you like to Hit or Stand? [H / S]\n')
    if hit.upper() == "H":
        blackjack_cards = player_chose_hit(blackjack, blackjack_cards)
        if blackjack.calculate_value_of_hand(blackjack_cards[0]) < 21:
            blackjack.display_value_of_players_hand(blackjack_cards)
            hit_or_stand(blackjack, blackjack_cards)
        else:
            decide_winner(blackjack, blackjack_cards)
    else:
        decide_winner(blackjack, blackjack_cards)


def player_chose_hit(blackjack, blackjack_cards):
    blackjack_cards = blackjack.deal_card_to_player(blackjack_cards)
    blackjack.calculate_value_of_hand(blackjack_cards[0])
    blackjack.dealer_card_if_less_than_17(blackjack_cards)
    return blackjack_cards


def decide_winner(blackjack, blackjack_cards):
    if blackjack.is_player_winner(blackjack_cards):
        blackjack.display_value_of_hands(blackjack_cards)
        print('Player Wins')
    elif blackjack.is_draw(blackjack_cards):
        blackjack.display_value_of_hands(blackjack_cards)
        print('Draw')
    else:
        blackjack.display_value_of_hands(blackjack_cards)
        print('Dealer Wins')


# create a deck [CLASS]
class Deck:

    def __init__(self, number_of_decks):
        values = ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"]
        suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
        self.cards = [{'value': value, 'suit': suit} for value in values for suit in suits] * number_of_decks


# create a card [CLASS]
class Card:

    def __init__(self, card):
        self.card = card

    # set card representation to readable format
    def __repr__(self):
        return f'{self.card["value"]} of {self.card["suit"]}'


# play game [CLASS]
class Blackjack:

    def __init__(self):
        self.blackjack_deck = Deck(1)
        self.record_win = 0
        self.record_loss = 0

    # convert card values to integer
    @staticmethod
    def card_value_to_int(card_as_string):
        value = card_as_string.card['value']
        if value == 'Jack' or value == 'Queen' or value == 'King':
            return 10
        elif value == 'Ace':
            return 11
        else:
            return int(value)

    # place starting game cards
    def begin_game(self):
        players_cards = [Card(self.deal()), Card(self.deal())]
        dealers_cards = [Card(self.deal()), Card(self.deal())]
        return players_cards, dealers_cards

    # deal cards to dealers hand if hand total is less than 17
    def dealer_card_if_less_than_17(self, playing_cards):
        while self.calculate_value_of_hand(playing_cards[1]) < 17:
            self.deal_card_to_dealer(playing_cards)
        return playing_cards

    # deal one card to player's hand
    def deal_card_to_player(self, playing_cards):
        player_card = Card(self.deal())
        players_cards = playing_cards[0]
        players_cards.append(player_card)
        return players_cards, playing_cards[1]

    # deal one card to dealer's hand
    def deal_card_to_dealer(self, playing_cards):
        dealer_card = Card(self.deal())
        dealers_cards = playing_cards[1]
        dealers_cards.append(dealer_card)
        return playing_cards[0], dealers_cards

    # deal one card
    def deal(self):
        deal_card = self.blackjack_deck.cards.pop()
        return deal_card

    # return True if player starting cards are blackjack
    def is_blackjack(self, playing_cards):
        players_hand = self.calculate_value_of_hand(playing_cards[0])
        if players_hand == 21:
            print(f'Blackjack\nPlayer\'s cards are: {playing_cards[0]}, Hand value is: {players_hand}')
            return True
        else:
            print(f'Player\'s cards are: {playing_cards[0]}, Hand value is: {players_hand}')
            print(f'Dealer\'s first card is: {playing_cards[1][0]}')
            return False

    # calculate hand value
    def calculate_value_of_hand(self, hand):
        hand_as_list_of_integers = [self.card_value_to_int(card) for card in hand]
        if 11 in hand_as_list_of_integers:
            if sum(hand_as_list_of_integers) >= 21:
                ace_is_one = [card if card != 11 else 1 for card in hand_as_list_of_integers]
                return sum(ace_is_one)
            else:
                return sum(hand_as_list_of_integers)
        else:
            return sum(hand_as_list_of_integers)

    # display value of hand to player
    def display_value_of_players_hand(self, playing_cards):
        players_hand = self.calculate_value_of_hand(playing_cards[0])
        print(f'Player\'s cards are: {playing_cards[0]}, Hand value is: {players_hand}')
        print(f'Dealer\'s first card is: {playing_cards[1][0]}')

    # display value of both hands
    def display_value_of_hands(self, playing_cards):
        players_hand = self.calculate_value_of_hand(playing_cards[0])
        dealers_hand = self.calculate_value_of_hand(playing_cards[1])
        print(f'Player\'s cards are: {playing_cards[0]}, Hand value is: {players_hand}')
        print(f'Dealer\'s cards are: {playing_cards[1]}, Hand value is: {dealers_hand}')

    # return True if game is a draw
    def is_draw(self, playing_cards):
        players_hand = self.calculate_value_of_hand(playing_cards[0])
        dealers_hand = self.calculate_value_of_hand(playing_cards[1])
        if players_hand == dealers_hand:
            return True

    # return True if player is the winner
    def is_player_winner(self, playing_cards):
        players_hand = self.calculate_value_of_hand(playing_cards[0])
        dealers_hand = self.calculate_value_of_hand(playing_cards[1])
        if players_hand <= 21 and dealers_hand <= 21:
            return players_hand > dealers_hand
        elif dealers_hand > 21 and players_hand <= 21:
            return True

    # shuffle the deck
    def shuffle(self):
        deck_length = len(self.blackjack_deck.cards)
        for index_a in range(deck_length):
            index_b = floor(randint(0, deck_length - 1))
            card_a = self.blackjack_deck.cards[index_a]
            self.blackjack_deck.cards[index_a] = self.blackjack_deck.cards[index_b]
            self.blackjack_deck.cards[index_b] = card_a
        return self.blackjack_deck.cards

    # calculate deck length
    def deck_length(self):
        return len(self.blackjack_deck.cards)


if __name__ == '__main__':
    main()
