from enums import PlayerAction
from enums import Rank

class Player:
    """Represents a player in the game."""
    
    def __init__(self, name, betAmount):
        self.name = name
        self.betAmount = betAmount
        self.totalGames = 0
        self.totalWinnings = 0
        self.losses = 0
        self.wins = 0
        self.hand = []
        
    def add_card(self, card):
        """Adds a card to the player's hand."""
        self.hand.append(card)

    def clear_hand(self):
        """Clear the players hand of all cards"""
        self.hand = []
        
    def hand_value(self):
        """Calculates the value of the player's hand, adjusting for Aces."""
        value = sum(card.value() for card in self.hand)
        aces = sum(1 for card in self.hand if card.rank == Rank.ACE)
        
        while value > 21 and aces:
            value -= 10
            aces -= 1
            
        return value
    
    def make_decision(self, dealer_up_card):
        """Makes the ideal decision (Hit or Stand) based on the current hand and the dealer's up card."""
        # Basic strategy logic can be implemented here
        # For simplicity, let's assume the player always hits if their hand value is less than 17
        if self.hand_value() < 17:
            return PlayerAction.HIT
        else:
            return PlayerAction.STAND
        
    def process_loss(self):
        self.losses += 1
        self.totalGames += 1
        self.totalWinnings -= self.betAmount

    def process_win(self):
        self.wins += 1
        self.totalGames += 1
        self.totalWinnings += self.betAmount

    def win_percentage(self):
        return "%.2f" % (self.wins / self.totalGames)
        