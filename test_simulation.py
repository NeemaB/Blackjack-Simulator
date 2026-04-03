from game import Game
import keyboard
from base_simulation import BaseSimulation

class TestSimulation(BaseSimulation):
    """Represents a simulation of a blackjack game"""

    def __init__(self, deck, players, isDebug=False):
        super().__init__(deck, players, isDebug)
        
    def run_simulation(self) -> None:
        game = Game(self._players, self._deck, isDebug=True)
        self.__play_round_with_message(game)
        keyboard.add_hotkey('space', lambda: self.__play_round_with_message(game))
        keyboard.wait()
        
    def __play_round_with_message(self, game : Game) -> None:
        print("******************Starting new round******************")
        game.play_round()
        self._numGames += 1
        print('\n')
        print('############################################')
        print('\n')
        for player in self._players:
            player.print_statistics_simple()  
        print('\n')
        print("Press 'space' to play the next round...")
                      
        
