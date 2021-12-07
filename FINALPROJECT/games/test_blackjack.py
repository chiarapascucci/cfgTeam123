from unittest import TestCase, main
from FINALPROJECT.games.blackjack import Deck, Blackjack, Card


class TestDeck(TestCase):

    def test_cards_created(self):
        new_deck = Deck(1)
        object_type = type([])
        object_length = 52
        deck_type = type(new_deck.cards)
        deck_length = len(new_deck.cards)
        self.assertEqual(object_length, deck_length)
        self.assertEqual(object_type, deck_type)

    def test_first_card_Ace_Hearts(self):
        new_deck = Deck(1)
        deck_first_card = new_deck.cards[0]
        deck_card_value = deck_first_card['value']
        deck_card_suit = deck_first_card['suit']
        self.assertEqual(deck_card_value, "Ace")
        self.assertEqual(deck_card_suit, "Hearts")

    def test_number_as_string(self):
        new_deck = Deck("1")
        object_type = type([])
        deck_type = type(new_deck.cards)
        self.assertEqual(object_type, deck_type)

    def test_make_100_decks(self):
        decks_100 = Deck(100)
        count_of_cards = 5200
        count_deck_cards = len(decks_100.cards)
        self.assertEqual(count_of_cards, count_deck_cards)

    def test_deck_cards_are_correct(self):
        new_deck = Deck(1)
        values = ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"]
        suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
        test_deck = [{'value': value, 'suit': suit} for value in values for suit in suits]
        self.assertEqual(new_deck.cards, test_deck)


class TestBeginGame(TestCase):

    def test_return_cards(self):
        new_blackjack_game = Blackjack()
        begin_game_cards = new_blackjack_game.begin_game()
        player_test_cards = ([Card({'value': 'King', 'suit': 'Spades'}), Card({'value': 'King', 'suit': 'Clubs'})])
        dealer_test_cards = ([Card({'value': 'King', 'suit': 'Diamonds'}), Card({'value': 'King', 'suit': 'Hearts'})])
        self.assertEqual(str(begin_game_cards[0]), str(player_test_cards))
        self.assertEqual(str(begin_game_cards[1]), str(dealer_test_cards))

    def test_starting_hand_is_blackjack(self):
        new_blackjack_game = Blackjack()
        player_cards = (Card({'value': 'Ace', 'suit': 'Spades'}), Card({'value': 'King', 'suit': 'Clubs'}))
        dealer_cards = (Card({'value': 'Ace', 'suit': 'Spades'}), Card({'value': 'King', 'suit': 'Clubs'}))
        game_cards = player_cards, dealer_cards
        starting_hand_blackjack = new_blackjack_game.is_blackjack(game_cards)
        self.assertTrue(starting_hand_blackjack)

    def test_calculate_value_of_hand(self):
        new_blackjack_game = Blackjack()
        begin_game_cards = new_blackjack_game.begin_game()
        value_of_hand = new_blackjack_game.calculate_value_of_hand(begin_game_cards[0])
        self.assertEqual(value_of_hand, 20)

    def test_shuffle_method(self):
        new_blackjack_game = Blackjack()
        pre_shuffled_cards = new_blackjack_game.blackjack_deck.cards[0], new_blackjack_game.blackjack_deck.cards[1]
        new_blackjack_game.shuffle()
        post_shuffled_cards = new_blackjack_game.blackjack_deck.cards[0], new_blackjack_game.blackjack_deck.cards[1]
        self.assertNotEqual(pre_shuffled_cards, post_shuffled_cards)



if __name__ == '__main__':
    main()
