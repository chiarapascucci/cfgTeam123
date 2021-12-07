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
        playing_cards = new_blackjack_game.begin_game()
        player_test_cards = [Card({'value': 'King', 'suit': 'Spades'}), Card({'value': 'King', 'suit': 'Clubs'})]
        dealer_test_cards = [Card({'value': 'King', 'suit': 'Diamonds'}), Card({'value': 'King', 'suit': 'Hearts'})]
        self.assertEqual(str(playing_cards[0]), str(player_test_cards))
        self.assertEqual(str(playing_cards[1]), str(dealer_test_cards))

    def test_starting_hand_is_blackjack(self):
        new_blackjack_game = Blackjack()
        player_cards = [Card({'value': 'Ace', 'suit': 'Spades'}), Card({'value': 'King', 'suit': 'Clubs'})]
        dealer_cards = [Card({'value': 'Ace', 'suit': 'Spades'}), Card({'value': 'King', 'suit': 'Clubs'})]
        playing_cards = player_cards, dealer_cards
        starting_hand_blackjack = new_blackjack_game.is_blackjack(playing_cards)
        self.assertTrue(starting_hand_blackjack)

    def test_starting_hand_is_not_blackjack(self):
        new_blackjack_game = Blackjack()
        player_cards = [Card({'value': '9', 'suit': 'Clubs'}), Card({'value': 'Ace', 'suit': 'Spades'})]
        dealer_cards = [Card({'value': 'Ace', 'suit': 'Spades'}), Card({'value': 'King', 'suit': 'Clubs'})]
        playing_cards = player_cards, dealer_cards
        starting_hand_blackjack = new_blackjack_game.is_blackjack(playing_cards)
        self.assertFalse(starting_hand_blackjack)

    def test_calculate_value_of_hand(self):
        new_blackjack_game = Blackjack()
        playing_cards = new_blackjack_game.begin_game()
        value_of_hand = new_blackjack_game.calculate_value_of_hand(playing_cards[0])
        self.assertEqual(value_of_hand, 20)

    def test_shuffle_method(self):
        new_blackjack_game = Blackjack()
        pre_shuffled_cards = new_blackjack_game.blackjack_deck.cards[0], new_blackjack_game.blackjack_deck.cards[1]
        new_blackjack_game.shuffle()
        post_shuffled_cards = new_blackjack_game.blackjack_deck.cards[0], new_blackjack_game.blackjack_deck.cards[1]
        self.assertNotEqual(pre_shuffled_cards, post_shuffled_cards)


class TestDealMethods(TestCase):

    def test_deal_card_to_player(self):
        new_blackjack_game = Blackjack()
        playing_cards = new_blackjack_game.begin_game()
        playing_cards = new_blackjack_game.deal_card_to_player(playing_cards)
        self.assertEqual(len(playing_cards[0]), 3)

    def test_deal_card_to_dealer(self):
        new_blackjack_game = Blackjack()
        playing_cards = new_blackjack_game.begin_game()
        playing_cards = new_blackjack_game.deal_card_to_dealer(playing_cards)
        self.assertEqual(len(playing_cards[1]), 3)

    def test_deal_one_card(self):
        new_blackjack_game = Blackjack()
        dealt_card = new_blackjack_game.deal()
        self.assertEqual(dealt_card, {'value': 'King', 'suit': 'Spades'})

    def test_dealer_card_hand_less_than_17(self):
        new_blackjack_game = Blackjack()
        player_cards = [Card({'value': '2', 'suit': 'Spades'}), Card({'value': 'King', 'suit': 'Clubs'})]
        dealer_cards = [Card({'value': '2', 'suit': 'Spades'}), Card({'value': 'King', 'suit': 'Clubs'})]
        playing_cards = player_cards, dealer_cards
        playing_cards = new_blackjack_game.dealer_card_if_less_than_17(playing_cards)
        self.assertEqual(len(playing_cards[1]), 3)

class TestCalculateWinner(TestCase):

    def test_is_draw(self):
        new_blackjack_game = Blackjack()
        player_cards = [Card({'value': '2', 'suit': 'Spades'}), Card({'value': 'King', 'suit': 'Clubs'})]
        dealer_cards = [Card({'value': '2', 'suit': 'Spades'}), Card({'value': 'King', 'suit': 'Clubs'})]
        playing_cards = player_cards, dealer_cards
        is_hand_draw = new_blackjack_game.is_draw(playing_cards)
        self.assertTrue(is_hand_draw)

    def test_is_not_draw(self):
        new_blackjack_game = Blackjack()
        player_cards = [Card({'value': '3', 'suit': 'Spades'}), Card({'value': 'King', 'suit': 'Clubs'})]
        dealer_cards = [Card({'value': '2', 'suit': 'Spades'}), Card({'value': 'King', 'suit': 'Clubs'})]
        playing_cards = player_cards, dealer_cards
        is_hand_draw = new_blackjack_game.is_draw(playing_cards)
        self.assertFalse(is_hand_draw)

    def test_is_player_winner(self):
        new_blackjack_game = Blackjack()
        player_cards = [Card({'value': '10', 'suit': 'Spades'}), Card({'value': 'King', 'suit': 'Clubs'})]
        dealer_cards = [Card({'value': '2', 'suit': 'Spades'}), Card({'value': 'King', 'suit': 'Clubs'})]
        playing_cards = player_cards, dealer_cards
        is_players_hand_winning = new_blackjack_game.is_player_winner(playing_cards)
        self.assertTrue(is_players_hand_winning)

    def test_is_player_not_winner(self):
        new_blackjack_game = Blackjack()
        player_cards = [Card({'value': '2', 'suit': 'Spades'}), Card({'value': 'King', 'suit': 'Clubs'})]
        dealer_cards = [Card({'value': '10', 'suit': 'Spades'}), Card({'value': 'King', 'suit': 'Clubs'})]
        playing_cards = player_cards, dealer_cards
        is_players_hand_winning = new_blackjack_game.is_player_winner(playing_cards)
        self.assertFalse(is_players_hand_winning)

    def test_player_not_winner_over_21(self):
        new_blackjack_game = Blackjack()
        player_cards = [Card({'value': '10', 'suit': 'Spades'}), Card({'value': 'King', 'suit': 'Clubs'}),
                        Card({'value': 'King', 'suit': 'Clubs'})]
        dealer_cards = [Card({'value': '10', 'suit': 'Spades'}), Card({'value': 'King', 'suit': 'Clubs'})]
        playing_cards = player_cards, dealer_cards
        is_players_hand_winning = new_blackjack_game.is_player_winner(playing_cards)
        self.assertFalse(is_players_hand_winning)




if __name__ == '__main__':
    main()
