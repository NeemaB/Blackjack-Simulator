from strategies.chart_strategy import ChartStrategy
from strategies.default_strategy import DefaultStrategy

class StrategyFactory:

    def __init__(self, config):
        self.config = config

    def get_strategy_from_name(self, name=None):
        if name == "Chart":
            return ChartStrategy(self.config.splitEnabled, self.config.doubleDownEnabled, self.config.ddasEnabled)
        elif name == "Default":
            return DefaultStrategy()
        
        return DefaultStrategy()
        