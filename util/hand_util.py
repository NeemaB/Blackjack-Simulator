from util.enums import Rank

def num_soft_aces(hand):
    """Calculates the number of aces still considered as '11' in the player's hand"""
    value = sum(card.value() for card in hand)
    aces = sum(1 for card in hand if card.rank == Rank.ACE)
        
    while value > 21 and aces:
        value -= 10
        aces -= 1

    return aces

def hand_value(hand):
    """Calculates the value of the player's hand, adjusting for Aces."""
    value = sum(card.value() for card in hand)
    aces = sum(1 for card in hand if card.rank == Rank.ACE)
        
    while value > 21 and aces:
        value -= 10
        aces -= 1
            
    return value