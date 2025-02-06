from game import Game

class Simulation:
    """Represents a simulation of a blackjack game"""

    def __init__(self, numDecks, players, numGames):
        self.numDecks = numDecks
        self.players = players
        self.numGames = numGames

    def run_simulation(self):
        game = Game(self.players, self.numDecks)
        for _ in range(self.numGames):
            game.play_round()
        
        for player in self.players:
            print(f"Player: {player.name}, winnings: ${player.totalWinnings}, total wins: {player.wins}, total losses: {player.losses}, win ratio: {player.win_percentage()}")