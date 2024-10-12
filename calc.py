import csv

from utils.shoe import Shoe

def test_wr(case_size):
    wins = 0
    pushes = 0
    hands = 0
    losses = 0
    
    for i in range(case_size):

        decks = 6 #input("How many decks: ")
        shoe = Shoe(decks)
        while len(shoe.cards) > 15:
            dealer_hand = [shoe.draw()]
            player_hand = [shoe.draw(), shoe.draw()]

            if 'A' in player_hand or 'A' in dealer_hand:
                continue
            
            player_value = player_hand[0] + player_hand[1]
            dealer_value = dealer_hand[0]

            if player_value == 15 and dealer_value == 9 and shoe.get_true_count() > -1 and shoe.get_true_count() < 1:
                hands += 1

                while player_value < 17:
                    player_next_card = shoe.draw()
                    if player_next_card == 'A':
                        player_value += 1
                    else:
                        player_value += player_next_card

                
                if player_value < 22:
                    #players did not bust 
                    while dealer_value < 17:
                        # dealer draw a card
                        next_card = shoe.draw()
                        if next_card == 'A':
                            if dealer_value == 9:
                                # dealer 20
                                dealer_value = 20
                                break
                            else: dealer_value += 1
                        else:
                            dealer_value += next_card
                        
                    if dealer_value > 21 or player_value > dealer_value:
                        # dealer bust
                        # you win :)
                        wins += 1
                    elif dealer_value == player_value:
                        pushes += 1
                    else:
                        # dealer didnt bust
                        # dealer value is greater than player value
                        losses += 1

                else:
                    losses += 1
                        
                


    wr = wins/(losses)
    
    print(wr)
    print(hands)

    # with open('wins.csv', 'w') as file:
    #     writer = csv.writer(file)
    #     writer.writerows(won_hands)
    return 


def test_A_odds(case_size):
    all_ace = 0
    for n in range(case_size):
        shoe = Shoe(6)
        aces = 0
        while shoe.decks_remaining > 1:
            if shoe.draw() == 'A':
                aces += 1
            if aces == 24:
                all_ace += 1
                break 

    return (all_ace/case_size) * 100
                   


if __name__ == '__main__':
   test_wr(100000000)