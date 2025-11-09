from player import Player
from game import Game
from simulation import Simulation
from test_simulation import TestSimulation
from simulation_config import SimulationConfig
from strategies.strategy_factory import StrategyFactory
import argparse  # Add this import

# Example usage
if __name__ == "__main__":
    # Add argument parsing
    parser = argparse.ArgumentParser(description='Blackjack simulation')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    args = parser.parse_args()
    
    isDebug = args.debug
    
    config = SimulationConfig.from_json('config.json')
    players = []

    strategyFactory = StrategyFactory(config)

    for player in config.players:
        players.append(Player(
            player['name'], 
            player['betAmount'], 
            strategyFactory.get_strategy_from_name(player['strategy'])))
    
    if isDebug:
        simulation = TestSimulation(config.numDecks, players, config.shuffleRatio, config.isContinuousShuffle)
    else:
        simulation = Simulation(config.numDecks, players, config.numGames, config.shuffleRatio, config.isContinuousShuffle)
    simulation.run_simulation()