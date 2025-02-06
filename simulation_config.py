import json

class SimulationConfig:
    """Represents the configuration for the Blackjack simulation."""
    
    def __init__(self, numDecks, players, numGames):
        self.numDecks = numDecks
        self.players = players  # List of dictionaries with 'name' and 'betAmount'
        self.numGames = numGames
    
    @classmethod
    def from_json(cls, file_path):
        """Loads the configuration from a JSON file."""
        with open(file_path, 'r') as file:
            config_data = json.load(file)
        return cls(
            numDecks=config_data['numDecks'],
            players=config_data['players'],
            numGames=config_data['numGames']
        )
    
    def __repr__(self):
        return (f"SimulationConfig(numDecks={self.numDecks}, "
                f"players={self.players}, numGames={self.numGames})")