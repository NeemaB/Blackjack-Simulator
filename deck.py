from enums import Rank, Suit
from card import Card
import random

class Deck:
    """Represents a deck of 52 cards."""
    
    def __init__(self, numDecks):
        self.cards = []
        
        for suit in Suit:
            for rank in Rank:
                for _ in range(numDecks):
                    self.cards.append(Card(suit, rank))
                
    def shuffle(self):
        """Shuffles the deck."""
        random.shuffle(self.cards)
        
    def deal_card(self):
        """Deals a single card from the deck."""
        return self.cards.pop()