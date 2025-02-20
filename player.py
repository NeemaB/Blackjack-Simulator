from enums import PlayerAction, PlayerType
from enums import Rank

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
        self.hand = []
        
    def add_card(self, card):
        """Adds a card to the player's hand."""
        self.hand.append(card)

    def clear_hand(self):
        """Clear the players hand of all cards"""
        self.hand = []

    def num_cards(self):
        """Calculate the number of cards in the player's hand"""
        return len(self.hand)

    def num_soft_aces(self):
        """Calculates the number of aces still considered as '11' in the player's hand"""
        value = sum(card.value() for card in self.hand)
        aces = sum(1 for card in self.hand if card.rank == Rank.ACE)
        
        while value > 21 and aces:
            value -= 10
            aces -= 1

        return aces
        
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
        return self.strategy.calc_player_action(dealer_up_card, self.hand_value(), self.num_soft_aces())
    
    def process_blackjack(self):
        """Handles the case where the player receives a blackjack from the first two cards 
           and wins the round """
        self.wins += 1
        self.totalGames += 1
        self.totalWinnings += self.betAmount * 1.5
        
    def process_loss(self): 
        """Handles the scenario where the player loses a round"""
        self.losses += 1
        self.totalGames += 1
        self.totalWinnings -= self.betAmount

    def process_win(self):
        """Handles the scenario where the player wins a round"""
        self.wins += 1
        self.totalGames += 1
        self.totalWinnings += self.betAmount

    def process_draw(self):
        """Handles the scenario where the player draws with the dealer"""
        self.totalGames += 1
        self.draws += 1

    def win_percentage(self):
        return "%.2f" % (self.wins / self.totalGames)
        