from abc import ABC, abstractmethod

class BaseSimulation(ABC):
    def __init__(self, deck, players, isDebug=False):
        self._deck = deck
        self._players = players
        self._isDebug = isDebug
        
        self._numGames = 0
        
    @abstractmethod
    def run_simulation(self) -> None:
        pass
      
    def get_results(self):
        """Returns structured results for reporting."""
        return {
            'players': [player.get_statistics() for player in self._players],
            'totalGames': self._numGames,
            'configuration': {
                'numDecks': self._deck.get_num_decks(),
                'shuffleRatio': self._deck.get_shuffle_ratio(),
                'isContinuousShuffle': self._deck.get_is_continuous_shuffle()
            }
        }
        
        