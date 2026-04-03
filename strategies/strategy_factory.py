from strategies.chart_strategy import ChartStrategy
from strategies.default_strategy import DefaultStrategy
from strategies.probability_strategy import ProbabilityStrategy

class StrategyFactory:

    def __init__(self, config, deck, isDebug):
        self._config = config
        self._deck = deck
        self._isDebug = isDebug

    def get_strategy_from_name(self, name=None):
        if name == "Chart":
            return ChartStrategy(self._config.splitEnabled, self._config.doubleDownEnabled, self._config.ddasEnabled)
        elif name == "Default":
            return DefaultStrategy()
        elif name == "Probability":
            return ProbabilityStrategy(self._config.splitEnabled, self._config.doubleDownEnabled, self._config.ddasEnabled, self._deck, self._isDebug)
        
        return DefaultStrategy()
        