# A card is dealt to the player facing upwards (visible to everyone).
# The dealer deals a card to himself visible to everyone.
# Another card is given to the player facing upwards.
# The dealer deals a card facing downwards for himself.
# The player has to decide whether to stand with the current set of cards or get another card.
# If the player decides to hit, another card is dealt.
# If the player decides to stand, then the dealer reveals his hidden card.
# The dealer does not have the authority to decide whether to hit or stand. The general rule is that the dealer needs to keep hitting more cards if the sum of dealer’s cards is less than 17.
# As soon as the sum of dealer’s cards is either 17 or more, the dealer is obliged to stand.
# According to the final sum of the cards, the winner is decided.

from random import randint
from math import floor

# create a deck [CLASS]
class Deck:

    def __init__(self):
        self.cards = []

    # create new deck method
    def create_deck(self):
        values = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
        suits = ["hearts", "diamonds", "clubs", "spades"]
        for value in values:
            for suit in suits:
                card = {'value': value, 'suit': suit}
                self.cards.append(card)
        return self.cards

    #create shuffle method
    def shuffle(self):
        deck_length = len(self.cards)
        for index_a in range(deck_length):
            index_b = floor(randint(0, deck_length - 1))
            card_a = self.cards[index_a]
            self.cards[index_a] = self.cards[index_b]
            self.cards[index_b] = card_a
        return self.cards

new_deck = Deck()
new_deck.create_deck()
print(new_deck.cards)
new_deck.shuffle()
print(new_deck.cards)
