from random import shuffle
import math

from utils.deck import Deck

high_cards = ['A',10]
low_cards = [2,3,4,5,6]

class Shoe:
    def __init__(self, decks):
        self.decks_remaining = decks
        self.running_count = 0
        self.cards = []
        for i in range(decks):
            deck = Deck()
            self.cards += deck.cards
        shuffle(self.cards)

        self.burn_card = self.draw()
        

    def draw(self):
        card = self.cards.pop()
        if card in high_cards:
            self.running_count -= 1
        elif card in low_cards:
            self.running_count += 1

        self.decks_remaining = self.get_decks_remaining()

        return card
    
    def get_decks_remaining(self):
        # # Round to the highest half deck 
        # # ex 48 cards remaining = 1 deck remaining
        # # ex2 53 cards remaining = 1.5 decks remaining
        # return math.ceil((len(self.cards) / 52) * 2) / 2

        # its a float but its fine. truncating in get_true_count
        return (len(self.cards) / 52)

    def get_true_count(self):
        return math.floor(self.running_count/self.decks_remaining)


    