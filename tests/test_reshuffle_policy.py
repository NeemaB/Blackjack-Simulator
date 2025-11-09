from deck import Deck
import pytest

from util.enums import Suit

@pytest.mark.parametrize(
    "testShuffleRatio, testNumDecks",
    [
      (0.5, 1),
      (0.5, 2),
      (0.5, 3),
      (0.5, 4),
      (0.75, 1),
      (0.75, 2),
      (0.25, 3),
      (0.25, 4)
    ], 
)
def test_reshuffle_policy(testShuffleRatio, testNumDecks):

  deck = Deck(numDecks=testNumDecks, shuffleRatio=testShuffleRatio)
  for _ in range(int(testNumDecks * 52 * testShuffleRatio) + 1):
    deck.deal_card()
  deck.reset()
  assert len(deck.get_available_cards()) == testNumDecks * 52
       
  for rank in range(2, 10):    
    assert sum(1 for card in deck.get_available_cards() if card.value() == rank) == 4 * testNumDecks, "Failed for rank {}".format(rank)      
  assert sum(1 for card in deck.get_available_cards() if card.value() == 10) == 16 * testNumDecks, "Failed for rank 10"
  assert sum(1 for card in deck.get_available_cards() if card.value() == 11) == 4 * testNumDecks, "Failed for rank Ace"
  
  for suit in range(1, 4):
    assert sum(1 for card in deck.get_available_cards() if card.suit == Suit(suit)) == 13 * testNumDecks, "Failed for suit {}".format(suit)
  
  for _ in range(int(testNumDecks * 52 * testShuffleRatio) - 1):
    deck.deal_card()
  deck.reset()
  assert len(deck.get_available_cards()) == testNumDecks * 52 - (int(testNumDecks * 52 * testShuffleRatio) - 1)
  
          
        
        