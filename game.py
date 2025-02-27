from util.constants import MAIN_HAND, SPLIT_HAND
from util.enums import PlayerAction, PlayerType
from deck import Deck
from player import Player

class Game:
    """Represents a game of Blackjack."""
    
    def __init__(self, players, numDecks, shuffleRatio, isDebug=False):
        self.__deck = Deck(numDecks, shuffleRatio)
        self.__players = players
        self.__dealer = Player("Dealer", 0, None, playerType=PlayerType.DEALER)
        self.__isDebug = isDebug

    def __reset(self):
        """Resets the game by determining whether a reshuffle is required or not"""
        self.__deck.reset()
        for player in self.__players:
            player.reset()
        self.__dealer.reset()
        
    def __deal_initial_cards(self):
        """Deals two initial cards to each player and the dealer."""
        for _ in range(2):
            for player in self.__players:
                player.add_card(self.__deck.deal_card())
        self.__dealer.add_card(self.__deck.deal_card()) # Dealer only has one visible card until all players have played
        
        # Add debug output
        if self.__isDebug:
            print("\n=== Initial Hands ===")
            for player in self.__players:
                print(f"{player.name}: {player.get_hand(MAIN_HAND)}")
            print(f"Dealer: {self.__dealer.get_hand(MAIN_HAND)}")
            print("===================\n")

    def __debug_print_hands(self, player, decision):
        """Prints debug information about a player's hands after a decision."""
        if self.__isDebug:
            print(f"\n=== {player.name}'s hands after {decision.name} ===")
            for h in range(len(player.hands)):
                print(f"Hand {h}: {player.get_hand(h)}")
            print("==================\n")

    def __play_hand(self, player, hand=MAIN_HAND):
        """Handles a player playing a hand recursively until their turn is done"""
        decision = player.make_decision(self.__dealer.hand_value(), hand)
        if self.__isDebug:
            print(f"Player {player.name} decision: {decision.name}")
            
        if decision == PlayerAction.HIT:
            player.add_card(self.__deck.deal_card(), hand)
            self.__debug_print_hands(player, decision)
        elif decision == PlayerAction.DOUBLE_DOWN:
            # Only a single card can be added to a hand after doubling down
            player.double_down(hand)
            player.add_card(self.__deck.deal_card(), hand)
            self.__debug_print_hands(player, decision)
            return
        elif decision == PlayerAction.SPLIT:
            # Split into two hands and play each independently
            player.split()
            # Split on aces, add only a single card to each hand then end turn
            if player.hand_value(MAIN_HAND) == 11:
                player.add_card(self.__deck.deal_card(), MAIN_HAND)
                player.add_card(self.__deck.deal_card(), SPLIT_HAND)
                self.__debug_print_hands(player, decision)
                return
            
            # Otherwise add card to each hand and continue playing if possible
            player.add_card(self.__deck.deal_card(), MAIN_HAND)
            player.add_card(self.__deck.deal_card(), SPLIT_HAND)
            if player.hand_value(MAIN_HAND) < 21:
                self.__play_hand(player, MAIN_HAND)
            if player.hand_value(SPLIT_HAND) < 21:
                self.__play_hand(player, SPLIT_HAND)

            self.__debug_print_hands(player, decision)
            return
        elif decision == PlayerAction.STAND:
            self.__debug_print_hands(player, decision)
            return
        if player.hand_value(hand) < 21:
            self.__play_hand(player, hand)            
            
    def play_round(self):
        """Plays a round of Blackjack."""
        self.__deal_initial_cards()
        
        # Players take their turns
        for player in self.__players:
            self.__play_hand(player)
                    
        # Dealer's turn
        while self.__dealer.hand_value() < 17:
            self.__dealer.add_card(self.__deck.deal_card())
        
        if self.__isDebug:
            print(f"Dealer hand: {self.__dealer.get_hand(MAIN_HAND)}")
            
        # Determine the outcome for each player
        for player in self.__players:
            for hand in range(len(player.hands)):
                if player.hand_value(hand) > 21:
                    player.process_loss(hand)
                    if self.__isDebug:
                        print(f"Player {player.name} lost hand {hand} with hand {player.get_hand(hand)}")
                elif self.__dealer.hand_value() > 21 or player.hand_value(hand) > self.__dealer.hand_value():
                    if player.hand_value(hand) == 21 and player.num_cards(hand) == 2 and len(player.hands) == 1:
                        player.process_blackjack()
                        if self.__isDebug:
                            print(f"Player {player.name} won hand {player.get_hand(hand)} with blackjack")
                    else:
                        player.process_win(hand)
                        if self.__isDebug:
                            print(f"Player {player.name} won hand {hand} with hand {player.get_hand(hand)}")
                elif player.hand_value(hand) == self.__dealer.hand_value():
                    player.process_draw()
                    if self.__isDebug:
                        print(f"Player {player.name} drew hand {hand} with hand {player.get_hand(hand)}")
                else:
                    player.process_loss(hand)
                    if self.__isDebug:
                        print(f"Player {player.name} lost hand {hand} with hand {player.get_hand(hand)}")

        self.__reset()
    