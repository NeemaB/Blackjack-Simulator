import argparse
from pathlib import Path

from .domain.deck import Deck
from .domain.player import Player
from .reporting.generator import ReportGenerator
from .simulation.config import SimulationConfig
from .simulation.manual import ManualSimulation
from .simulation.runner import SimulationRunner
from .strategies.factory import StrategyFactory

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CONFIG_PATH = PROJECT_ROOT / "configs" / "default.json"


def main() -> None:
    """Main entry point for the blackjack simulation."""
    parser = argparse.ArgumentParser(description="Blackjack simulation")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    parser.add_argument(
        "--report",
        type=str,
        default=None,
        help="Generate HTML report to the specified file",
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=DEFAULT_CONFIG_PATH,
        help="Path to configuration file",
    )
    parser.add_argument("--test", action="store_true", help="Enable manual test simulation")
    args = parser.parse_args()

    config = SimulationConfig.from_json(args.config)
    deck = Deck(config.numDecks, config.shuffleRatio, config.isContinuousShuffle)
    strategy_factory = StrategyFactory(config, deck, args.debug)
    players = [
        Player(
            player["name"],
            player["betAmount"],
            strategy_factory.get_strategy_from_name(player.get("strategy")),
        )
        for player in config.players
    ]

    if args.test:
        simulation = ManualSimulation(deck, players, args.debug)
    else:
        simulation = SimulationRunner(deck, players, config.numGames, args.debug)

    simulation.run_simulation()

    if args.report:
        results = simulation.get_results()
        report_path = Path(args.report)

        try:
            report_generator = ReportGenerator()
            report_generator.generate_report(results, config.to_dict(), report_path)
            print(f"\n{'=' * 60}")
            print(f"HTML report successfully generated: {report_path}")
            print(f"{'=' * 60}\n")
        except Exception as exc:
            print(f"\n{'=' * 60}")
            print(f"Error generating report: {exc}")
            print(f"{'=' * 60}\n")
    else:
        for player in players:
            player.print_statistics_simple()
