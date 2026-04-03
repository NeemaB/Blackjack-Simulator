from ..domain.game import Game
from .base import BaseSimulation


class ManualSimulation(BaseSimulation):
    """Represents a simulation of a blackjack game"""

    def __init__(self, deck, players, isDebug=False):
        super().__init__(deck, players, isDebug)

    def run_simulation(self) -> None:
        game = Game(self._players, self._deck, self._isDebug)
        self.__play_round_with_message(game)

        while True:
            try:
                user_input = input("Press Enter to play the next round, or 'q' to quit: ")
            except (EOFError, KeyboardInterrupt):
                print("\nExiting manual simulation.")
                break

            if user_input.strip().lower() in {"q", "quit", "exit"}:
                print("Exiting manual simulation.")
                break

            self.__play_round_with_message(game)

    def __play_round_with_message(self, game: Game) -> None:
        print("******************Starting new round******************")
        game.play_round()
        self._numGames += 1
        print("\n")
        print("############################################")
        print("\n")
        for player in self._players:
            player.print_statistics_simple()
        print("\n")
