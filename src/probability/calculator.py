"""Probability helpers for player/dealer outcomes.
"""
from typing import TypedDict

from .stats_deck import StatsDeck

class DealerOutcomeProbs(TypedDict):
    win: float
    loss: float
    draw: float

class PlayerOutcomeProbs(TypedDict):
    win: float
    loss: float
    draw: float

def calc_dealer_probs_helper(
  stats_deck: StatsDeck,
  player_hand_value: int,
  dealer_hand_value: int,
  num_aces: int,
  cur_prob: float,
  outcome_probs: DealerOutcomeProbs) -> None:
    """Recursive helper function to calculate dealer probabilities.

    Args:
        stats_deck (StatsDeck): The current stats of the deck.
        player_hand_value (int): The value of the player's hand.
        dealer_upcard_value (int): The value of the dealer's upcard.
        num_aces (int): The number of aces counted as 11 in dealer's hand.
        probs (dict): Dictionary to accumulate probabilities.
    """
    for key in stats_deck.stats:
      if stats_deck.stats[key] == 0:
        continue
      
      if key == 11:
        num_aces += 1
      
      new_dealer_value = dealer_hand_value + key
      
      # Adjust for soft aces
      while new_dealer_value > 21 and num_aces > 0:
        new_dealer_value -= 10
        num_aces -= 1
      
      # Dealer busts
      if new_dealer_value > 21:
        outcome_probs["loss"] += cur_prob * (float(stats_deck.stats[key]) / stats_deck.total_cards)    
        continue
      
      # Dealer stands
      if new_dealer_value >= 17:
        if new_dealer_value > player_hand_value:
          outcome_probs["win"] += cur_prob * (float(stats_deck.stats[key]) / stats_deck.total_cards)
        elif new_dealer_value < player_hand_value:
          outcome_probs["loss"] += cur_prob * (float(stats_deck.stats[key]) / stats_deck.total_cards)
        else:
          outcome_probs["draw"] += cur_prob * (float(stats_deck.stats[key]) / stats_deck.total_cards)
        continue
      
      # Calculate probability of receiving current hand value
      outcome_prob = cur_prob * (float(stats_deck.stats[key]) / stats_deck.total_cards)
      
      # Dealer must hit again  
      stats_deck.remove_card(key)
      calc_dealer_probs_helper(
        stats_deck,
        player_hand_value,
        new_dealer_value,
        num_aces,
        outcome_prob,
        outcome_probs)
      
      stats_deck.add_card(key)
      
def calc_player_probs_hit(player_hand_value: int,
                           dealer_upcard_value: int,
                           stats_deck: StatsDeck) -> PlayerOutcomeProbs:
    """Calculates the probability of winning if the player hits.

    Args:
        player_hand_value (int): The value of the player's hand.
        dealer_upcard_value (int): The value of the dealer's upcard.
        stats_deck (StatsDeck): A statistical representation of the remaining deck.
    """

    dealer_outcome_probs: DealerOutcomeProbs = {
        "win": 0.0,
        "loss": 0.0,
        "draw": 0.0,
    }

    init_prob = 1.0

    for key in stats_deck.stats:
        if stats_deck.stats[key] == 0:
            continue

        new_player_value = player_hand_value + key

        # Player busts
        if new_player_value > 21:
            dealer_outcome_probs["win"] += init_prob * float(stats_deck.stats[key]) / stats_deck.total_cards
            continue

        outcome_prob = init_prob * (float(stats_deck.stats[key]) / stats_deck.total_cards)

        stats_deck.remove_card(key)
        calc_dealer_probs_helper(
            stats_deck,
            new_player_value,
            dealer_upcard_value,
            1 if dealer_upcard_value == 11 else 0,
            outcome_prob,
            dealer_outcome_probs,
        )
        stats_deck.add_card(key)

    player_outcome_probs: PlayerOutcomeProbs = {
        "win": dealer_outcome_probs["loss"],
        "loss": dealer_outcome_probs["win"],
        "draw": dealer_outcome_probs["draw"],
    }

    return player_outcome_probs
    
def calc_player_probs_no_hit(player_hand_value: int,
                             dealer_upcard_value: int,
                             stats_deck: StatsDeck) -> PlayerOutcomeProbs:
    """Calculates the probability of winning if the player does not hit.

    Args:
        player_hand_value (int): The value of the player's hand.
        dealer_upcard_value (int): The value of the dealer's upcard.
        stats_deck (StatsDeck): A statistical representation of the remaining deck.
    """

    dealer_outcome_probs: DealerOutcomeProbs = {
        "win": 0.0,
        "loss": 0.0,
        "draw": 0.0,
    }

    calc_dealer_probs_helper(
        stats_deck,
        player_hand_value,
        dealer_upcard_value,
        1 if dealer_upcard_value == 11 else 0,
        1.0,
        dealer_outcome_probs,
    )

    player_outcome_probs: PlayerOutcomeProbs = {
        "win": dealer_outcome_probs["loss"],
        "loss": dealer_outcome_probs["win"],
        "draw": dealer_outcome_probs["draw"],
    }

    return player_outcome_probs
    
    
    
    
    
    
      
      
        
