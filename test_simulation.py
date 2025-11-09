from game import Game


class TestSimulation:
    """Represents a simulation of a blackjack game"""
    TEST_ROUNDS = 2

    def __init__(self, numDecks, players, shuffleRatio, isContinuousShuffle=False):
        self.__numDecks = numDecks
        self.__players = players
        self.__shuffleRatio = shuffleRatio
        self.__isContinuousShuffle = isContinuousShuffle

    def run_simulation(self):
        game = Game(self.__players, self.__numDecks,
                    self.__shuffleRatio, self.__isContinuousShuffle, isDebug=True)
        for _ in range(TestSimulation.TEST_ROUNDS):
            game.play_round()

        print('\n')
        print('############################################')
        print('\n')
        for player in self.__players:
            print(f"Player: {player.name}, winnings: ${player.totalWinnings}, total wins: {player.wins}, total losses: {player.losses}, total draws: {TestSimulation.TEST_ROUNDS - player.losses - player.wins}, win ratio: {player.win_percentage()}")
