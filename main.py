from player import Player
from game import Game
from simulation import Simulation
from simulation_config import SimulationConfig

# Example usage
if __name__ == "__main__":
    config = SimulationConfig.from_json('config.json')
    players = []

    for player in config.players:
        players.append(Player(player['name'], player['betAmount']))

    simulation = Simulation(config.numDecks, players, config.numGames)
    simulation.run_simulation()