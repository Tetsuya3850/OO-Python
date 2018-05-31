from enum import Enum
from abc import ABCMeta, abstractmethod
from random import shuffle


class Suit(Enum):
    HEART = 0
    DIAMOND = 1
    CLUBS = 2
    SPADE = 3


class Card():
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit


class Hand():
    def __init__(self, deck):
        self.cards = []
        self.deck = deck

    def draw_card(self):
        card = self.deck.deal_card()
        self.cards.append(card)

    def score(self):
        total_value = 0
        for card in card:
            total_value += card.value
        return total_value


class BlackJackHand(Hand):
    BLACKJACK = 21

    def __init__(self, deck):
        super(BlackJackHand, self).__init__(deck)

    def show_hand(self):
        for card in self.cards:
            print(card.value, card.suit)

    def score(self):
        min_over = float('inf')
        max_under = float('-inf')
        for score in self.possible_scores():
            if score > self.BLACKJACK:
                min_over = min(min_over, score)
            elif score <= self.BLACKJACK:
                max_under = max(max_under, score)
        return max_under if max_under != float('-inf') else min_over

    def possible_scores(self):
        scores = [0]
        for card in self.cards:
            if card.value == 1:
                for i in range(len(scores)):
                    score = scores[i]
                    scores[i] += 1
                    scores.append(score + 11)
            else:
                for i in range(len(scores)):
                    scores[i] += card.value if card.value <= 10 else 10
        return scores


class Deck():
    def __init__(self):
        self.cards = [Card(i, suit) for suit in Suit for i in range(1, 14)]
        self.deal_index = 0
        shuffle(self.cards)

    def deal_card(self):
        if self.deal_index < len(self.cards):
            card = self.cards[self.deal_index]
            self.deal_index += 1
            return card
        else:
            print("Out of cards!")


class BlackJackGame:
    def __init__(self):
        self.deck = Deck()
        self.player = BlackJackHand(self.deck)
        self.start_game()

    def start_game(self):
        self.player.draw_card()
        self.player.draw_card()
        self.player.show_hand()
        print("Draw another card? Yes or No.")
        decision = input()
        while decision.lower() == 'yes':
            self.player.draw_card()
            self.player.show_hand()
            score = self.player.score()
            if score > 21:
                print("Failed! {0}".format(score))
                return
            print("Draw another card? Yes or No.")
            decision = input()
        print("Suucess! {0}".format(self.player.score()))


game = BlackJackGame()
