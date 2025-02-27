from util import hand_util
from util.enums import PlayerAction, PlayerType
from util.enums import Rank
from util.constants import MAIN_HAND, SPLIT_HAND

class Player:
    """Represents a player in the game."""
    
    def __init__(self, name, betAmount, strategy, playerType=PlayerType.REGULAR):
        self.name = name
        self.betAmount = betAmount  
        self.totalGames = 0
        self.totalWinnings = 0
        self.losses = 0
        self.wins = 0
        self.draws = 0
        self.strategy = strategy
        self.playerType = playerType
        self.isDoubleDown = [False, False]

        self.hands = []
        self.hands.append([])
        
    def add_card(self, card, hand=MAIN_HAND):
        """Adds a card to the player's hand."""
        self.hands[hand].append(card)

    def clear_hand(self):
        """Clear the players hand of all cards"""
        self.hands = []
        self.hands.append([])

    def num_cards(self, hand=MAIN_HAND):
        """Calculate the number of cards in the player's hand"""
        return len(self.hands[hand])

    def num_soft_aces(self, hand=MAIN_HAND):
        """Calculates the number of aces still considered as '11' in the player's hand"""
        return hand_util.num_soft_aces(self.hands[hand])
        
    def hand_value(self, hand=MAIN_HAND):
        """Calculates the value of the player's hand, adjusting for Aces."""
        return hand_util.hand_value(self.hands[hand])
    
    def get_hand(self, hand=MAIN_HAND):
        """Returns the player's hand"""
        return self.hands[hand]
    
    def make_decision(self, dealer_up_card, hand=MAIN_HAND):
        """Makes the ideal decision (Hit or Stand) based on the current hand and the dealer's up card."""
        return self.strategy.calc_player_action(
            dealer_up_card, 
            self.hands[hand], 
            self.num_soft_aces(hand), 
            len(self.hands) == 2)
    
    def split(self):
        """Handles player action where two identical cards are split into two separate hands that can be played independently"""
        self.hands.append([])
        self.hands[SPLIT_HAND].append(self.hands[MAIN_HAND].pop())
        self.isDoubleDown.append(False)

    def double_down(self, hand=MAIN_HAND):
        """Handles player action where bet amount is doubled after first two cards are revealed"""
        self.isDoubleDown[hand] = True

    def process_blackjack(self):
        """Handles the case where the player receives a blackjack from the first two cards 
           and wins the round """
        self.wins += 1
        self.totalGames += 1
        self.totalWinnings += self.betAmount * 1.5
        
    def process_loss(self, hand=MAIN_HAND): 
        """Handles the scenario where the player loses a round"""
        self.losses += 1
        self.totalGames += 1
        self.totalWinnings -= self.betAmount * 2 if self.isDoubleDown[hand] else self.betAmount

    def process_win(self, hand=MAIN_HAND):
        """Handles the scenario where the player wins a round"""
        self.wins += 1
        self.totalGames += 1
        self.totalWinnings += self.betAmount * 2 if self.isDoubleDown[hand] else self.betAmount

    def process_draw(self):
        """Handles the scenario where the player draws with the dealer"""
        self.totalGames += 1
        self.draws += 1

    def win_percentage(self):
        """Percentage of wins over all games"""
        return "%.2f" % (self.wins / self.totalGames)
    
    def reset(self):
        """Reset player after round is over"""
        self.clear_hand()
        self.isDoubleDown = [False, False]
        