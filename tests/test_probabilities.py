from util.probability import calc_player_probs_no_hit, calc_player_probs_hit
from deck import Deck
from card import Card
from util.stats_deck import StatsDeck 

def test_calc_player_probs_no_hit():
    # Create a deck with known composition
    statsDeck = StatsDeck()
    
    # One card of each rank value
    for rank in range(2, 12):
      statsDeck.add_card(rank)

    player_hand_value = 12 # Example player hand value
    dealer_upcard_value = 6 # Example dealer upcard value

    probs = calc_player_probs_no_hit(player_hand_value, dealer_upcard_value, statsDeck)
    
    print(probs)

    # Check that probabilities sum to 1
    total_prob = probs["probPlayerWin"] + probs["probPlayerLose"] + probs["probPlayerDraw"]
    assert abs(total_prob - 1.0) < 1e-6, "Probabilities do not sum to 1"

    # Check that individual probabilities are within valid range
    assert 0.0 <= probs["probPlayerWin"] <= 1.0, "Invalid probability for player win"
    assert 0.0 <= probs["probPlayerLose"] <= 1.0, "Invalid probability for player lose"
    assert 0.0 <= probs["probPlayerDraw"] <= 1.0, "Invalid probability for player draw"
  
def test_calc_player_probs_hit():
  statsDeck = StatsDeck()
  
  for rank in range(2, 12):
    statsDeck.add_card(rank)
    
  player_hand_value = 20 # Example player hand value
  dealer_upcard_value = 6 # Example dealer upcard value
  
  probs = calc_player_probs_hit(player_hand_value, dealer_upcard_value, statsDeck)
  
  print(probs)

  # Check that probabilities sum to 1
  total_prob = probs["probPlayerWin"] + probs["probPlayerLose"] + probs["probPlayerDraw"]
  assert abs(total_prob - 1.0) < 1e-6, "Probabilities do not sum to 1"

  # Check that individual probabilities are within valid range
  assert 0.0 <= probs["probPlayerWin"] <= 1.0, "Invalid probability for player win"
  assert 0.0 <= probs["probPlayerLose"] <= 1.0, "Invalid probability for player lose"
  assert 0.0 <= probs["probPlayerDraw"] <= 1.0, "Invalid probability for player draw"