from game import Game
from base_simulation import BaseSimulation

class Simulation(BaseSimulation):
    """Represents a simulation of a blackjack game"""

    def __init__(self, deck, players, totalGames, isDebug=False):
        super().__init__(deck, players, isDebug)
        
        self._totalGames = totalGames

    def run_simulation(self) -> None:
        game = Game(self._players, self._deck, self._isDebug)
        for i in range(self._totalGames):
            if i % (self._totalGames / 10) == 0:
                print('|', end='', flush=True)
            game.play_round()
            self._numGames += 1
          
        