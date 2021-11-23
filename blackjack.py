# A card is dealt to the player facing upwards (visible to everyone).
# The dealer deals a card to himself visible to everyone.
# Another card is given to the player facing upwards.
# The dealer deals a card facing downwards for himself.
# The player has to decide whether to stand with the current set of cards or get another card.
# If the player decides to hit, another card is dealt.
# If the player decides to stand, then the dealer reveals his hidden card.
# The dealer does not have the authority to decide whether to hit or stand.
# The general rule is that the dealer needs to keep hitting more cards if the sum of dealer’s cards is less than 17.
# As soon as the sum of dealer’s cards is either 17 or more, the dealer is obliged to stand.
# According to the final sum of the cards, the winner is decided.

from random import randint
from math import floor

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

    def __repr__(self):
        return f'{self.card["value"]} of {self.card["suit"]}'

# play game [CLASS]
class Blackjack:

    def __init__(self):
        self.blackjack_deck = Deck(1)

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
        player_card_1 = Card(self.deal())
        player_card_2 = Card(self.deal())
        dealer_card_1 = Card(self.deal())
        dealer_card_2 = Card(self.deal())
        players_cards = [player_card_1, player_card_2]
        dealers_cards = [dealer_card_1, dealer_card_2]
        return players_cards, dealers_cards

    # stand [reveal dealer card, and deal another card to dealer if less than 17]

    # deal another card to player
    def deal_card_to_player(self, starting_cards):
        player_card = Card(self.deal())
        players_cards = starting_cards[0]
        players_cards.append(player_card)
        return players_cards, starting_cards[1]

    # deal another card to dealer
    def deal_card_to_dealer(self, starting_cards):
        dealer_card = Card(self.deal())
        dealers_cards = starting_cards[1]
        dealers_cards.append(dealer_card)
        return starting_cards[0], dealers_cards

    # deal method
    def deal(self):
        deal_card = self.blackjack_deck.cards.pop()
        return deal_card

    # deck length method
    def deck_length(self):
        return len(self.blackjack_deck.cards)

    # is blackjack method
    def is_blackjack(self, starting_cards):
        players_hand = self.calculate_value_of_hand(starting_cards[0])
        if players_hand == 21:
            print(f'Blackjack\nPlayer\'s cards are: {starting_cards[0]}, Hand value is: {players_hand}')
            return True
        else:
            print(f'Player\'s cards are: {starting_cards[0]}, Hand value is: {players_hand} \nDealer\'s first card is: {starting_cards[1][0]}')
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


    # shuffle method
    def shuffle(self):
        deck_length = len(self.blackjack_deck.cards)
        for index_a in range(deck_length):
            index_b = floor(randint(0, deck_length - 1))
            card_a = self.blackjack_deck.cards[index_a]
            self.blackjack_deck.cards[index_a] = self.blackjack_deck.cards[index_b]
            self.blackjack_deck.cards[index_b] = card_a
        return self.blackjack_deck.cards

if __name__ == '__main__':
    print('Welcome to Blackjack')
    play_game = input('Would you like to play? [Y / N]\n')
    if play_game.upper() == "Y":
        new_game = Blackjack()
        new_game.shuffle()
        starting_blackjack_cards = new_game.begin_game()
        new_game.is_blackjack(starting_blackjack_cards)
        if not new_game.is_blackjack(starting_blackjack_cards):
            deal_another_player_card = input('Would you like to Hit or Stand? [Hit / Stand]\n')
            if deal_another_player_card.upper() == "HIT":
                card_dealt_to_player = new_game.deal_card_to_player(starting_blackjack_cards)
                new_game.calculate_value_of_hand(starting_blackjack_cards[0])
                new_game.deal_card_to_dealer(card_dealt_to_player)
        else:
            print('You Won! Goodbye')
    else:
        print('Goodbye')




