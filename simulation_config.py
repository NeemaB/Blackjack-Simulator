import json

class SimulationConfig:
    """Represents the configuration for the Blackjack simulation."""
    
    def __init__(self, numDecks, players, numGames, shuffleRatio, doubleDownEnabled, 
                 splitEnabled, ddasEnabled, isContinuousShuffle=False):
        self.numDecks = numDecks
        self.players = players  # List of dictionaries with 'name' and 'betAmount'
        self.numGames = numGames
        self.shuffleRatio = shuffleRatio
        self.doubleDownEnabled = doubleDownEnabled
        self.splitEnabled = splitEnabled
        self.ddasEnabled = ddasEnabled
        self.isContinuousShuffle = isContinuousShuffle
        # New field for strategy comparison configuration
            
    @classmethod
    def from_json(cls, file_path):
        """Loads the configuration from a JSON file."""
        with open(file_path, 'r') as file:
            config_data = json.load(file)
        return cls(
            numDecks=config_data['numDecks'],
            players=config_data['players'],
            numGames=config_data['numGames'],
            shuffleRatio=config_data['shuffleRatio'],
            doubleDownEnabled=config_data['doubleDownEnabled'],
            splitEnabled=config_data['splitEnabled'],
            ddasEnabled=config_data['ddasEnabled'],
            isContinuousShuffle=config_data.get('isContinuousShuffle', config_data.get('continuousShuffler', False)),
        )
    
    def to_dict(self):
        """Returns configuration as a dictionary for reporting."""
        return {
            'numDecks': self.numDecks,
            'numGames': self.numGames,
            'shuffleRatio': self.shuffleRatio,
            'splitEnabled': self.splitEnabled,
            'doubleDownEnabled': self.doubleDownEnabled,
            'ddasEnabled': self.ddasEnabled,
            'isContinuousShuffle': self.isContinuousShuffle,
            'players': self.players
          }
    
    def __repr__(self):
        return (f"SimulationConfig(numDecks={self.numDecks}, "
                f"players={self.players}, "
                f"numGames={self.numGames})")