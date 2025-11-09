from game import Game

class Simulation:
    """Represents a simulation of a blackjack game"""

    def __init__(self, numDecks, players, numGames, shuffleRatio, isContinuousShuffle=False):
        self.__numDecks = numDecks
        self.__players = players
        self.__numGames = numGames
        self.__shuffleRatio = shuffleRatio
        self.__isContinuousShuffle = isContinuousShuffle

    def run_simulation(self):
        game = Game(self.__players, self.__numDecks, self.__shuffleRatio, self.__isContinuousShuffle)
        for i in range(self.__numGames):
            if i % (self.__numGames / 10) == 0:
                print('|', end='', flush=True)
            game.play_round()
        
        print('\n')
        print('############################################')
        print('\n')
        for player in self.__players:
            print(f"Player: {player.name}, winnings: ${player.totalWinnings}, total wins: {player.wins}, total losses: {player.losses}, total draws: {self.__numGames - player.losses - player.wins}, win ratio: {player.win_percentage()}")