from enum import Enum

class Suit(Enum):
    HEARTS = 1
    SPADES = 2
    CLUBS = 3
    DIAMONDS = 4

class PlayerAction(Enum):
    HIT = 1
    STAND = 2

class Rank(Enum):
    ACE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    JACK = 10
    QUEEN = 11
    KING = 12


    