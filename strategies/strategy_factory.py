from strategies.chart_strategy import ChartStrategy
from strategies.default_strategy import DefaultStrategy
from strategies.probability_strategy import ProbabilityStrategy
from strategies.comparison_strategy import ComparisonStrategy

class StrategyFactory:

    def __init__(self, config, deck=None):
        self.config = config
        self.deck = deck
        self.comparison_strategies = []  # Track all comparison strategies created

    def get_strategy_from_name(self, name=None):
        """Creates a strategy based on the name, with optional comparison tracking."""
        base_strategy = self._create_base_strategy(name)
        
        # Check if strategy comparison is enabled and applicable
        if (self.config.strategyComparison.get('enabled', False) and 
            name in ['Chart', 'Probability']):
            
            # Get the comparison mode
            mode = self.config.strategyComparison.get('mode', 'chart_vs_probability')
            
            if mode == 'chart_vs_probability':
                if name == 'Chart':
                    comparison = self._create_base_strategy('Probability')
                    wrapper = ComparisonStrategy(base_strategy, comparison, 'Chart', 'Probability')
                elif name == 'Probability':
                    comparison = self._create_base_strategy('Chart')
                    wrapper = ComparisonStrategy(base_strategy, comparison, 'Probability', 'Chart')
                else:
                    return base_strategy
                    
                self.comparison_strategies.append(wrapper)
                return wrapper
            
            # Could add other comparison modes here (e.g., 'all_vs_default')
        
        return base_strategy
    
    def _create_base_strategy(self, name):
        """Creates the base strategy without any comparison wrapper."""
        if name == "Chart":
            return ChartStrategy(self.config.splitEnabled, self.config.doubleDownEnabled, self.config.ddasEnabled)
        elif name == "Default":
            return DefaultStrategy()
        elif name == "Probability":
            return ProbabilityStrategy(self.config.splitEnabled, self.config.doubleDownEnabled, 
                                     self.config.ddasEnabled, self.deck)
        
        return DefaultStrategy()
    
    def get_comparison_stats(self):
        """Returns comparison statistics from all comparison strategies created."""
        return [strategy.get_comparison_stats() for strategy in self.comparison_strategies]