# Player logic for free bet


# TODO

from stratagies.free_bet_strat import strat

class Player_spot:
    def __init__(self, shoe, dealer_card):
        self.shoe = shoe
        self.dealer_card = dealer_card
        self.hands = [{
                "cards": [shoe.draw(), shoe.draw()],
                "type": "Real Hand",
                "wager": 1
            }
        ]
        self.split_count = 0
        self.split_aces = False
        # To keep track of player doubles
        self.bet_count = 1

    def play(self):
        playing = True
        current_hand = 0
        while playing:
            hand = self.hands[current_hand]
            # 1. Do we only have 1 card?
            if len(hand["cards"]) == 1:
                hand["cards"].append(self.shoe.draw())

            # X. Handle the splitting aces issue
            if self.split_count > 0 and hand["cards"][0] == 'A':
                if not hand["cards"][1] == 'A':
                    self.hands[current_hand]["result"] = hand["cards"][1] + 11
                    current_hand += 1

            # 2. Do we have a pair?
            if hand["cards"][0] == hand["cards"][1] and (not hand["cards"][0] == 5) and (not hand["cards"][0] == 10) and self.split_count < 3 and len(hand["cards"]) == 2:
                # We have a pair
                # a. Split our pair
                self.hands[current_hand]["cards"] = [hand["cards"][0]]
                self.hands[current_hand] = {
                    "cards": [hand["cards"][1]],
                    "type": "Free Hand",
                    "wager": 1
                }
                self.split_count += 1
                if hand["cards"][0] == 'A':
                    self.split_aces = True
                # b. since we only have one card in our current hand, we want to "play" this hand again
                continue
            # 3. Do we have an ace?
            elif 'A' in hand["cards"] and not self.split_aces:
                # a. Do we have Blackjack/21?
                if 10 in hand["cards"] and len(hand["cards"]) == 2:
                    # Blackjack
                    self.hands[current_hand]["result"] = "blackjack" if hand["type"] == "Real Hand" else 21
                    current_hand += 1
                # b. strip aces
                # Copy hand for modification
                hand_copy = hand["cards"][:]

                # Remove aces and keep track of how many we have
                ace_count = 0
                while 'A' in hand_copy:
                    ace_count += 1
                    hand_copy.remove('A')

                # c. Total remaining cards:
                remaining_value = 0
                for card in hand_copy:
                    remaining_value += card
                hand_total = ace_count + remaining_value

                # Is it a hard or soft total?
                if hand_total < 11:
                    # It is still a soft total
                    hand_total += 10
                    if hand_total < 16:
                        # Less than soft 16: hit
                        self.hands[current_hand]["cards"].append(self.shoe.draw())
                        continue
                    else:
                        # More than soft 16
                        if hand_total > 18 and hand["type"] == "Real Hand":
                            # Soft 19 or 20 on real hand: stand
                            self.hands[current_hand]["result"] = hand_total
                            current_hand += 1
                        else:
                            # Soft 16 through 20 on free hand or soft 16 through 18 on real hand: dynamic
                            decision = strat[hand["type"]]["Soft Totals"][str(hand_total)][self.dealer_card]
                            if decision == "H":
                                self.hands[current_hand]["cards"].append(self.shoe.draw())
                                continue
                            elif decision == "D":
                                # Since this is not a 9-11, we have to pay to double this one
                                self.bet_count += 1
                                self.double(current_hand)
                                current_hand += 1
                            else:
                                # Stand
                                self.hands[current_hand]["result"] = hand_total
                                current_hand += 1
                elif hand_total == 11:
                    self.hands[current_hand]["result"] = 21
                    current_hand += 1
                else:
                    # Our hand value is too high to use an ace as 11
                    # Easiest solution I can think of is removing all the aces and replacing them with 1s
                    while 'A' in hand["cards"]:
                        self.hands[current_hand]["cards"].remove('A')
                        self.hands[current_hand]["cards"].append(1)
                    continue
            # 4. Just a hard total.
            else:
                # a. Get hand total
                hand_total = 0
                for card in hand["cards"]:
                    hand_total += card

                # b. rule out super low hands
                if hand_total < 9:
                    self.hands[current_hand]["cards"].append(self.shoe.draw())
                    continue
                # c. check for free double
                elif hand_total < 12:
                    self.double(current_hand)
                    current_hand += 1
                # d. Hand total is between 12 and 17
                elif hand_total < 18:
                    decision = strat[hand["type"]]["Hard Totals"][str(hand_total)][self.dealer_card]
                    if decision == "H":
                        self.hands[current_hand]["cards"].append(self.shoe.draw())
                        continue
                    elif decision == "S":
                        self.hands[current_hand]["result"] = hand_total
                        current_hand += 1
                    else:
                        # Surrender if possible
                        if self.split_count == 0 and len(hand["cards"]) == 2:
                            # Surrender allowed
                            self.hands[current_hand]["result"] = "surrender"
                            current_hand += 1
                        else:
                            if hand_total == 17:
                                # Stand
                                self.hands[current_hand]["result"] = hand_total
                                current_hand += 1
                            else:
                                # Hit
                                self.hands[current_hand]["cards"].append(self.shoe.draw())
                                continue

                # e. Hand total is between 18 and 21
                elif hand_total < 22:
                    # Stand
                    self.hands[current_hand]["result"] = hand_total
                    current_hand += 1
                # f. Bust
                else:
                    self.hands[current_hand]["result"] = "bust"
                    current_hand += 1

            if current_hand == len(self.hands):
                playing = False
        
        return self.hands

    def double(self, current_hand):
        last_card = self.shoe.draw()
        self.hands[current_hand]["cards"].append(last_card)
        self.hands[current_hand]["wager"] += 1
        cards = self.hands[current_hand]["cards"]
        total = 0
        # Check  for aces
        if 'A' in cards:
            ace_count = 0
            while 'A' in cards:
                cards.remove('A')
                ace_count += 1

            total = ace_count
            for card in cards:
                total += card

            if total < 12:
                total += 10
        else:
            for card in cards:
                total += card

        if total > 21:
            raise Exception("You busted on a double somehow, wp bro")
        
        self.hands[current_hand]["result"] = total


            
