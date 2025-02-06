import random
from enums import Suit, Rank

class Card:
    """Represents a single card in a deck."""
    
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        
    def __repr__(self):
        return f"{self.rank} of {self.suit}"
    
    def value(self):
        """Returns the value of the card in Blackjack."""
        if self.rank in [Rank.JACK, Rank.QUEEN, Rank.KING]:
            return 10
        elif self.rank == Rank.ACE:
            return 11  # Ace can be 11 or 1, but we'll handle that in the Player class
        else:
            return self.rank.value

    