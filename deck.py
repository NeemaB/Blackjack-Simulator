from util.enums import Rank, Suit
from card import Card
import random

class Deck:
    """Represents a deck of 52 cards."""
    
    def __init__(self, numDecks, shuffleRatio, isContinuousShuffle=False):
        self.__availableCards = []
        self.__dealtCards = []
        self.__discardedCards = []
        self.__totalCards = numDecks * 52
        self.__numDecks = numDecks
        self.__shuffleRatio = shuffleRatio
        self.__isContinuousShuffle = isContinuousShuffle
        self.__reshufflePending = False
        
        self.__initialize()

    def __initialize(self):
        """Initialize the deck by clearing all stacks of cards then populating the available cards based on the number of decks"""
        self.__availableCards.clear()
        self.__dealtCards.clear()
        self.__discardedCards.clear()

        for suit in Suit:
            for rank in Rank:
                for _ in range(self.__numDecks):
                    self.__availableCards.append(Card(suit, rank))

        self.__shuffle()
    
    
    def __shuffle(self):
        """Shuffles the deck."""
        random.shuffle(self.__availableCards)
    
    def get_available_cards(self):
        """Returns the available cards."""
        return self.__availableCards
    
    def deal_card(self):
        """Deals a single card from the deck."""
        if len(self.__availableCards) == 0:
            random.shuffle(self.__discardedCards)
            self.__availableCards += self.__discardedCards
            self.__discardedCards.clear()
            self.__reshufflePending = True

        card = self.__availableCards.pop()
        self.__dealtCards.append(card)
        return card
    
    def reset(self):
        """Handle a reset after a round has ended"""
        self.__discardedCards += self.__dealtCards
        self.__dealtCards.clear()
        
        if self.__isContinuousShuffle:
            # Continuous shuffler: reshuffle all cards after every round
            self.__initialize()
        elif self.__reshufflePending:
            self.__reshufflePending = False
            self.__initialize()
        elif (len(self.__discardedCards) / self.__totalCards) >= self.__shuffleRatio:
            self.__initialize()
        
