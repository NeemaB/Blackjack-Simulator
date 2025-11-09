from typing import List
from card import Card
from deck import Deck
from util.stats_deck import StatsDeck
from util.enums import PlayerAction
from util.hand_util import hand_value, num_soft_aces
from util.probability import (
    calc_player_probs_hit,
    calc_player_probs_no_hit
)

class ProbabilityStrategy():
    """
    A blackjack strategy that uses probability calculations to determine the best action.
    
    This strategy calculates expected values for different actions based on the
    probability of various outcomes and chooses the action with the highest
    expected value.
    """
    
    def __init__(self, split_enabled: bool = True, 
                 double_down_enabled: bool = True, 
                 ddas_enabled: bool = False,
                 deck: Deck = None):
        """
        Initialize the probability-based strategy.
        
        Args:
            split_enabled (bool): Whether splitting is allowed. Defaults to True.
            double_down_enabled (bool): Whether doubling down is allowed. Defaults to True.
            ddas_enabled (bool): Whether double down after split is allowed. Defaults to False.
            deck (Deck): The deck being used in the game. Defaults to None.
        """
        self.split_enabled = split_enabled
        self.double_down_enabled = double_down_enabled
        self.ddas_enabled = ddas_enabled
        self.deck = deck
    
    def calc_player_action(self, dealer_hand: List[Card], 
                          player_hand: List[Card], 
                          is_split: bool = False) -> PlayerAction:
        """
        Calculate the optimal player action based on probability analysis.
        
        Args:
            dealer_hand (List[Card]): The dealer's hand (typically just the up card).
            player_hand (List[Card]): The player's current hand.
            is_split (bool): Whether this hand is the result of a split. Defaults to False.
            
        Returns:
            PlayerAction: The recommended action based on probability calculations.
        """
        # Get basic hand information
        player_value = hand_value(player_hand)
        dealer_up_value = dealer_hand[0].value()
        
        # Create a StatsDeck representing current deck composition
        stats_deck = self._create_stats_deck()
        
        # Calculate expected values for each action
        ev_stand = self._calculate_stand_ev(player_value, dealer_up_value, stats_deck)
        ev_hit = self._calculate_hit_ev(player_value, dealer_up_value, stats_deck)
        
        # Initialize with basic options
        best_action = PlayerAction.STAND if ev_stand >= ev_hit else PlayerAction.HIT
        best_ev = max(ev_stand, ev_hit)
        
        # Check if double down is possible and calculate its EV
        if self._can_double_down(player_hand, is_split):
            ev_double = self._calculate_double_ev(player_value, dealer_up_value, stats_deck)
            if ev_double > best_ev:
                best_action = PlayerAction.DOUBLE_DOWN
                best_ev = ev_double
        
        # Check if split is possible and calculate its EV
        if self._can_split(player_hand, is_split):
            ev_split = self._calculate_split_ev(player_hand, dealer_up_value, stats_deck)
            if ev_split > best_ev:
                best_action = PlayerAction.SPLIT
                best_ev = ev_split
        
        return best_action
    
    def _create_stats_deck(self) -> StatsDeck:
        """Create a StatsDeck representing remaining cards in the deck."""
        return StatsDeck(self.deck)
    
    def _calculate_stand_ev(self, player_value: int, 
                           dealer_up_value: int, 
                           stats_deck: StatsDeck) -> float:
        """Calculate expected value of standing."""
        if player_value > 21:
            return -1.0  # Already busted
        
        probs = calc_player_probs_no_hit(player_value, dealer_up_value, stats_deck)
        
        # Calculate expected value: win = +1, loss = -1, push = 0
        ev = probs.get('win', 0.0) - probs.get('loss', 0.0)
        return ev
    
    def _calculate_hit_ev(self, player_value: int, 
                         dealer_up_value: int, 
                         stats_deck: StatsDeck) -> float:
        """Calculate expected value of hitting."""
        if player_value >= 21:
            return -1.0  # No point in hitting
        
        probs = calc_player_probs_hit(player_value, dealer_up_value, stats_deck)
        
        # Calculate expected value
        ev = probs.get('win', 0.0) - probs.get('loss', 0.0)
        return ev
    
    def _calculate_double_ev(self, player_value: int, 
                            dealer_up_value: int, 
                            stats_deck: StatsDeck) -> float:
        """Calculate expected value of doubling down."""
        # Double down means double the bet, so multiply EV by 2
        # But you can only take one more card
        hit_probs = calc_player_probs_hit(player_value, dealer_up_value, stats_deck)
        ev = (hit_probs.get('win', 0.0) - hit_probs.get('loss', 0.0)) * 2.0
        return ev
    
    # TODO: FIX IMPLEMENTATION: calculate probability of hit for one card only and double
    #       to get the appropriate EV in the case of no double down. Factor double down after
    #       split as well
    def _calculate_split_ev(self, player_hand: List[Card], 
                           dealer_up_value: int, 
                           stats_deck: StatsDeck) -> float:
        """
        Calculate expected value of splitting using probability calculations.
        
        Compares the EV of playing the current hand versus playing two split hands.
        """
        # First, calculate the EV of NOT splitting (playing the current hand)
        current_hand_value = hand_value(player_hand)
        ev_no_split_stand = self._calculate_stand_ev(current_hand_value, 
                                                     dealer_up_value, 
                                                     stats_deck)
        ev_no_split_hit = self._calculate_hit_ev(current_hand_value, 
                                                 dealer_up_value, 
                                                 stats_deck)
        ev_no_split = max(ev_no_split_stand, ev_no_split_hit)
        
        # Now calculate the EV of splitting
        # Each split hand starts with one card of the pair
        single_card_value = player_hand[0].value()
        
        # For aces, we typically get only one card per split hand
        if single_card_value == 1:
            # Special handling for split aces
            # Most casinos only allow one card per ace
            split_hand_value = 11  # Ace counts as 11 initially
            ev_single_ace = self._calculate_split_ace_ev(split_hand_value, 
                                                         dealer_up_value, 
                                                         stats_deck)
            # Two hands with the same EV
            ev_split = 2 * ev_single_ace
        else:
            # For non-aces, calculate EV of playing out each split hand
            # Start with the single card value
            if single_card_value == 10:  # Face cards and 10s
                starting_value = 10
            else:
                starting_value = single_card_value
            
            # Calculate the best EV for a hand starting with this card
            ev_single_hand = self._calculate_split_hand_ev(starting_value, 
                                                           dealer_up_value, 
                                                           stats_deck)
            
            # Two hands with the same expected value
            ev_split = 2 * ev_single_hand
        
        return ev_split
    
    def _calculate_split_ace_ev(self, starting_value: int, 
                               dealer_up_value: int, 
                               stats_deck: StatsDeck) -> float:
        """
        Calculate EV for a split ace (which typically gets only one card).
        """
        # For split aces, we get exactly one more card and must stand
        # Calculate probabilities for all possible resulting hands
        total_ev = 0.0
        total_cards = stats_deck.total_cards
        
        # Consider each possible card we could draw
        for card_value in range(1, 11):  # Cards values 1-10
            card_count = stats_deck.stats.get(card_value, 0)
            if card_count == 0:
                continue
            
            # Probability of drawing this card
            prob_card = card_count / total_cards
            
            # Calculate the resulting hand value
            if card_value == 1:  # Another ace
                # Two aces = 12 (one counts as 11, one as 1)
                final_value = 12
            else:
                final_value = 11 + card_value
                if final_value > 21:  # Bust, ace becomes 1
                    final_value = 1 + card_value
            
            # Get probabilities for this final hand
            probs = calc_player_probs_no_hit(final_value, dealer_up_value, stats_deck)
            hand_ev = probs.get('win', 0.0) - probs.get('loss', 0.0)
            
            # Add weighted EV
            total_ev += prob_card * hand_ev
        
        return total_ev
    
    def _calculate_split_hand_ev(self, starting_value: int, 
                                dealer_up_value: int, 
                                stats_deck: StatsDeck) -> float:
        """
        Calculate EV for a split hand (non-ace) that can be played normally.
        """
        # For a split hand starting with a single card, we need to consider
        # all possible sequences of play
        
        # Simplified approach: assume we draw one card and then make optimal decision
        total_ev = 0.0
        total_cards = stats_deck.total_cards
        
        for card_value in range(1, 11):  # Card values 1-10
            card_count = stats_deck.stats.get(card_value, 0)
            if card_count == 0:
                continue
            
            # Probability of drawing this card
            prob_card = card_count / total_cards
            
            # Calculate the resulting hand value
            if card_value == 1:  # Ace
                # Best use of ace (11 if possible, 1 if not)
                hand_value_with_ace_11 = starting_value + 11
                if hand_value_with_ace_11 <= 21:
                    resulting_value = hand_value_with_ace_11
                else:
                    resulting_value = starting_value + 1
            else:
                resulting_value = starting_value + card_value
            
            if resulting_value > 21:
                # Busted
                hand_ev = -1.0
            else:
                # Make optimal decision for this 2-card hand
                ev_stand = self._calculate_stand_ev(resulting_value, 
                                                    dealer_up_value, 
                                                    stats_deck)
                ev_hit = self._calculate_hit_ev(resulting_value, 
                                                dealer_up_value, 
                                                stats_deck)
                hand_ev = max(ev_stand, ev_hit)
            
            # Add weighted EV
            total_ev += prob_card * hand_ev
        
        return total_ev
    
    def _can_double_down(self, player_hand: List[Card], 
                        is_split: bool) -> bool:
        """Check if doubling down is allowed."""
        if not self.double_down_enabled:
            return False
        
        if len(player_hand) != 2:
            return False
        
        if is_split and not self.ddas_enabled:
            return False
        
        return True
    
    def _can_split(self, player_hand: List[Card], 
                  is_split: bool) -> bool:
        """Check if splitting is allowed."""
        if not self.split_enabled:
            return False
        
        if is_split:  # Can't split again
            return False
        
        if len(player_hand) != 2:
            return False
        
        # Check if both cards have the same rank
        return player_hand[0].value() == player_hand[1].value()