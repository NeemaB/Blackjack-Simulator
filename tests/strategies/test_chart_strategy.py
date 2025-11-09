from card import Card
from strategies.chart_strategy import ChartStrategy
from util.enums import PlayerAction, Rank, Suit

class TestChartStrategy:
    def test_calc_player_action(self):
        strategy = ChartStrategy(splitEnabled=True, doubleDownEnabled=True, ddasEnabled=True)
        player_hand = [Card(Suit.HEARTS, Rank.ACE), Card(Suit.CLUBS, Rank.TWO)]
        dealer_hand = [Card(Suit.DIAMONDS, Rank.SIX)]
        
        assert strategy.calc_player_action(dealer_hand, player_hand, False) == PlayerAction.DOUBLE_DOWN
        
    def test_calc_player_action_2(self):
        strategy = ChartStrategy(splitEnabled=True, doubleDownEnabled=True, ddasEnabled=True)
        player_hand = [Card(Suit.HEARTS, Rank.FOUR), Card(Suit.CLUBS, Rank.JACK)]
        dealer_hand = [Card(Suit.DIAMONDS, Rank.ACE)]
        
        assert strategy.calc_player_action(dealer_hand, player_hand, False) == PlayerAction.HIT




