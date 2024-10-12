# To test the winrate at each true count for free bet black jack
from configs.free_bet_config import constants 
from utils.shoe import Shoe
from utils.round import Round

def main():
    for i in range(constants["sample size"]):
        shoe = Shoe(constants["decks"])

        while shoe.decks_remaining >= 1:
            round = Round(shoe, constants["spots"])
            players_spots = round.players_turn()
            # Plater hands is a list of lists of objects containing the following proporties
            # cards: a list of cards in the hand
            # type: either "Real Hand" or "Free Hand"
            # wager: an integer representing the value of the hand 1 or 2
            # result: integer of the hand if it is less than 22, "blackjack", or "bust"
            if player:
                dealers_hand = round.dealers_turn()
                for hand in players_hands:
                    if hand[]



