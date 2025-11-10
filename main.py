from player import Player
from game import Game
from simulation import Simulation
from test_simulation import TestSimulation
from simulation_config import SimulationConfig
from strategies.strategy_factory import StrategyFactory
from report.report_generator import ReportGenerator
from deck import Deck
import argparse

def main():
    """Main entry point for the blackjack simulation."""
    # Add argument parsing
    parser = argparse.ArgumentParser(description='Blackjack simulation')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    parser.add_argument('--report', type=str, default=None, help='Generate HTML report to specified file')
    parser.add_argument('--config', type=str, default='config.json', help='Path to configuration file')
    args = parser.parse_args()
    
    isDebug = args.debug
    
    # Load configuration
    config = SimulationConfig.from_json(args.config)
    players = []

    # Create a deck instance if needed for probability strategy
    deck = Deck(config.numDecks, config.shuffleRatio, config.isContinuousShuffle) if any(
        p.get('strategy') == 'Probability' for p in config.players
    ) else None
    
    # Create players with their strategies
    strategyFactory = StrategyFactory(config, deck)
    for player in config.players:
        players.append(Player(
            player['name'], 
            player['betAmount'], 
            strategyFactory.get_strategy_from_name(player['strategy'])))
    
    # Run simulation
    if isDebug:
        simulation = TestSimulation(config.numDecks, players, config.shuffleRatio, config.isContinuousShuffle)
    else:
        simulation = Simulation(config.numDecks, players, config.numGames, config.shuffleRatio, config.isContinuousShuffle)
    
    results = simulation.run_simulation()
    
    # Add strategy comparison stats to results if available
    comparison_stats = strategyFactory.get_comparison_stats()
    if comparison_stats:
        results['strategy_comparisons'] = comparison_stats
    
    # Generate report if requested
    if args.report:
        try:
            report_gen = ReportGenerator()
            report_gen.generate_report(results, config.to_dict(), args.report)
            print(f"\n{'='*60}")
            print(f"✓ HTML Report successfully generated: {args.report}")
            print(f"{'='*60}\n")
        except Exception as e:
            print(f"\n{'='*60}")
            print(f"✗ Error generating report: {str(e)}")
            print(f"{'='*60}\n")

if __name__ == "__main__":
    main()