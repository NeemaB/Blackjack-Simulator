from strategies.chart_strategy import ChartStrategy
from strategies.default_strategy import DefaultStrategy

class StrategyFactory:

    @classmethod
    def get_strategy_from_name(self, name=None):
        if name == "Chart":
            return ChartStrategy()
        elif name == "Default":
            return DefaultStrategy()
        
        return DefaultStrategy()
        