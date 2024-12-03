# Author: Jonathan Rajarathinam
# Email: jrajarathina@umass.edu
# Spire ID: 34685791

import random

def deal_cards():
    cards = [2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K", "A"]
    return random.choice(cards)

def calc_count(hand):
    count = 0
    aces = 0
    for card in hand:
        if card in ["J", "Q", "K"]:
            count += 10
        elif card == "A":
            aces += 1
            count += 11
        else:
            count += card
    while count > 21 and aces:
        count -= 10
        aces -= 1
    return count

def can_double_down(hand):
    count = calc_count(hand)
    no_aces = [card for card in hand if card != "A"]
    no_aces_count = sum(10 if card in ["J", "Q", "K"] else card for card in no_aces)
    return (count in [9, 10, 11] and "A" not in hand) or (16 <= count <= 18 and "A" in hand and no_aces_count == count - 11)

def play():
    total_money = 1000
    while total_money > 0:
        print(f"\nYou have ${total_money}")
        while True:
            try:
                bet = int(input("Enter your bet amount: "))
                if 0 < bet <= total_money:
                    break
                print("Invalid bet amount.")
            except ValueError:
                print("Please enter a valid number.")
        
        player_hand = [deal_cards(), deal_cards()]
        dealer_hand = [deal_cards(), deal_cards()]
        
        print(f"\nYour Cards: {player_hand} Current Count: {calc_count(player_hand)}")
        print(f"Dealer's First Card: {dealer_hand[0]}")
        
        doubled_down = False
        while calc_count(player_hand) < 21:
            if can_double_down(player_hand):
                hs = input("Type 'h' to hit, 's' to stand, or 'dd' to double down: ").lower()
            else:
                hs = input("Type 'h' to hit or 's' to stand: ").lower()

            if hs == "h":
                player_hand.append(deal_cards())
                print(f"\nYour Cards: {player_hand} New Count: {calc_count(player_hand)}")
            elif hs == "dd" and can_double_down(player_hand):
                player_hand.append(deal_cards())
                print(f"\nYour Cards: {player_hand} Final Count: {calc_count(player_hand)}")
                bet *= 2
                doubled_down = True
                break
            else:
                break

        while calc_count(dealer_hand) < 17:
            dealer_hand.append(deal_cards())
        
        player_count = calc_count(player_hand)
        dealer_count = calc_count(dealer_hand)
        
        print(f"\nYour Final Hand: {player_hand} Final Count: {player_count}")
        print(f"Dealer's Final Hand: {dealer_hand} Final Count: {dealer_count}")
        
        if player_count > 21:
            print("Player Bust! Dealer Wins! :(")
            total_money -= bet
        elif dealer_count > 21:
            print("Dealer Bust! You Win! :)")
            total_money += bet * (4 if doubled_down else 2)
        elif player_count > dealer_count:
            print("You Win! :)")
            total_money += bet * (4 if doubled_down else 2)
        elif player_count < dealer_count:
            print("Dealer Wins! :(")
            total_money -= bet
        else:
            print("It's a Push!")
        
        if total_money == 0:
            print("\nYou're out of money!")
            break

        print("\nThank you for playing this round!")

play()
