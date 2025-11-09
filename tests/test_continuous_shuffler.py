from deck import Deck
import pytest
from util.enums import Suit

@pytest.mark.parametrize(
    "testNumDecks",
    [1, 2, 3, 4]
)
def test_continuous_shuffler_resets_after_each_round(testNumDecks):
    """Test that continuous shuffler returns all cards to deck after each round"""
    deck = Deck(numDecks=testNumDecks, shuffleRatio=0.5, isContinuousShuffle=True)
    
    initial_available = len(deck.get_available_cards())
    assert initial_available == testNumDecks * 52
    
    # Deal some cards
    for _ in range(10):
        deck.deal_card()
    
    # After dealing, available cards should be reduced
    assert len(deck.get_available_cards()) == testNumDecks * 52 - 10
    
    # After reset, all cards should be back in the deck
    deck.reset()
    assert len(deck.get_available_cards()) == testNumDecks * 52
    
    # Verify all card ranks are present
    for rank in range(2, 10):    
        assert sum(1 for card in deck.get_available_cards() if card.value() == rank) == 4 * testNumDecks, "Failed for rank {}".format(rank)      
    assert sum(1 for card in deck.get_available_cards() if card.value() == 10) == 16 * testNumDecks, "Failed for rank 10"
    assert sum(1 for card in deck.get_available_cards() if card.value() == 11) == 4 * testNumDecks, "Failed for rank Ace"
    
    # Verify all suits are present
    for suit in range(1, 4):
        assert sum(1 for card in deck.get_available_cards() if card.suit == Suit(suit)) == 13 * testNumDecks, "Failed for suit {}".format(suit)

@pytest.mark.parametrize(
    "testNumDecks, testRounds",
    [
        (1, 5),
        (2, 5),
        (3, 3),
        (4, 3)
    ]
)
def test_continuous_shuffler_multiple_rounds(testNumDecks, testRounds):
    """Test that continuous shuffler works consistently over multiple rounds"""
    deck = Deck(numDecks=testNumDecks, shuffleRatio=0.5, isContinuousShuffle=True)
    
    for round_num in range(testRounds):
        # Deal varying number of cards each round
        cards_to_deal = 10 + (round_num * 5)
        for _ in range(cards_to_deal):
            deck.deal_card()
        
        # Reset and verify all cards are back
        deck.reset()
        assert len(deck.get_available_cards()) == testNumDecks * 52, f"Round {round_num} failed"


@pytest.mark.parametrize(
    "testNumDecks",
    [1, 2, 4]
)
def test_continuous_shuffler_with_heavy_usage(testNumDecks):
    """Test continuous shuffler with heavy card usage approaching deck exhaustion"""
    deck = Deck(numDecks=testNumDecks, shuffleRatio=0.5, isContinuousShuffle=True)
    
    # Deal almost all cards (leaving just 5)
    cards_to_deal = testNumDecks * 52 - 5
    for _ in range(cards_to_deal):
        deck.deal_card()
    
    assert len(deck.get_available_cards()) == 5
    
    # Reset should return all cards
    deck.reset()
    assert len(deck.get_available_cards()) == testNumDecks * 52
