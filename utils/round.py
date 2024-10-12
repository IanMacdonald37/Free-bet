from utils.player_spot import Player_spot

class Round:
    def __init__(self, shoe, num_player_hands=1):
        self.shoe = shoe
        self.num_player_hands = num_player_hands

        self.count = self.shoe.get_true_count()
        self.dealer_hand = [self.shoe.draw()]

        self.player_spots = []
        for i in range(self.player_spots):
            self.player_spots[i] = Player_spot(self.dealer_hand[0])


    def players_turn(self):
        results = []
        for spot in self.player_spots:
            results.append(spot.play())

        return results

    def dealers_turn(self):
        dealer_total = 0
        drawing = True
        while drawing:
            self.dealer_hand += self.shoe.draw()
            if 'A' in self.dealer_hand:
                # Dealer has a soft total
                # 1. Copy hand to modify
                dealer_hand_copy = self.dealer_hand[:]

                # 2. Remove aces and keep track of how many we have
                ace_count = 0
                while 'A' in dealer_hand_copy:
                    ace_count += 1
                    dealer_hand_copy.remove('A')

                # 3. Total remaining cards:
                remaining_value = 0
                for card in dealer_hand_copy:
                    remaining_value += card
                dealer_total = ace_count + remaining_value

                # 4. Is it a hard or soft total?
                if dealer_total < 11:
                    # It is still a soft total
                    dealer_total += 10
                    if dealer_total > 17:
                        drawing = False
                elif dealer_total == 11:
                    # Dealer has soft 21 or Blackjack
                    if len(self.dealer_hand) == 2:
                        # Dealer Blackjack
                        dealer_total = "BJ"
                    else:
                        dealer_total = 21
                else:
                    # Dealer has a hard total
                    # Remove Aces for remaining draw simplicity
                    for i in range(len(self.dealer_hand)):
                        if self.dealer_hand[i] == 'A':
                            self.dealer_hand[i] = 1

                    dealer_total = 0
                    for card in self.dealer_hand:
                        dealer_total += card

                    if dealer_total > 16:
                        drawing = False
            else:
                dealer_total = 0
                for card in self.dealer_hand:
                    dealer_total += card

                if dealer_total >= 17:
                    drawing = False
        
        return dealer_total



