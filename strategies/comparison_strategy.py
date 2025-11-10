from util.enums import PlayerAction
from collections import defaultdict

class ComparisonStrategy():
    """
    Wrapper strategy that compares decisions between two strategies while using one as the primary.
    Tracks when strategies disagree on actions.
    """
    
    def __init__(self, primary_strategy, comparison_strategy, primary_name="Primary", comparison_name="Comparison"):
        """
        Args:
            primary_strategy: The strategy whose decisions will be used
            comparison_strategy: The strategy to compare against
            primary_name: Name of the primary strategy for tracking
            comparison_name: Name of the comparison strategy for tracking
        """
        self.primary_strategy = primary_strategy
        self.comparison_strategy = comparison_strategy
        self.primary_name = primary_name
        self.comparison_name = comparison_name
        
        # Track differences
        self.total_decisions = 0
        self.disagreements = 0
        self.disagreement_details = defaultdict(lambda: defaultdict(int))
        
    def calc_player_action(self, dealer_hand, player_hand, is_split=False):
        """Calculate action using primary strategy while tracking differences with comparison strategy."""
        primary_action = self.primary_strategy.calc_player_action(dealer_hand, player_hand, is_split)
        comparison_action = self.comparison_strategy.calc_player_action(dealer_hand, player_hand, is_split)
        
        self.total_decisions += 1
        
        if primary_action != comparison_action:
            self.disagreements += 1
            # Track what each strategy chose when they disagreed
            disagreement_key = f"{primary_action.name}_vs_{comparison_action.name}"
            self.disagreement_details[disagreement_key]['count'] += 1
            self.disagreement_details[disagreement_key]['primary_action'] = primary_action.name
            self.disagreement_details[disagreement_key]['comparison_action'] = comparison_action.name
            
        return primary_action
    
    def get_comparison_stats(self):
        """Returns statistics about strategy comparisons."""
        agreement_rate = ((self.total_decisions - self.disagreements) / self.total_decisions * 100) if self.total_decisions > 0 else 100
        
        return {
            'primary_name': self.primary_name,
            'comparison_name': self.comparison_name,
            'total_decisions': self.total_decisions,
            'agreements': self.total_decisions - self.disagreements,
            'disagreements': self.disagreements,
            'agreement_rate': f"{agreement_rate:.2f}%",
            'disagreement_rate': f"{(100 - agreement_rate):.2f}%",
            'disagreement_details': dict(self.disagreement_details)
        }