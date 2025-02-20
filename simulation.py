from game import Game

class Simulation:
    """Represents a simulation of a blackjack game"""

    def __init__(self, numDecks, players, numGames):
        self.numDecks = numDecks
        self.players = players
        self.numGames = numGames

    def run_simulation(self):
        game = Game(self.players, self.numDecks)
        for i in range(self.numGames):
            if i % (self.numGames / 10) == 0:
                print('|', end='', flush=True)
            game.play_round()
        
        print('\n')
        print('############################################')
        print('\n')
        for player in self.players:
            print(f"Player: {player.name}, winnings: ${player.totalWinnings}, total wins: {player.wins}, total losses: {player.losses}, total draws: {self.numGames - player.losses - player.wins}, win ratio: {player.win_percentage()}")