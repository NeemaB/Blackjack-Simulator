from enums import PlayerAction
from deck import Deck
from player import Player

class Game:
    """Represents a game of Blackjack."""
    
    def __init__(self, players, numDecks):
        self.numDecks = numDecks
        self.deck = Deck(numDecks)
        self.deck.shuffle()
        self.players = players
        self.dealer = Player("Dealer", 0)

    def reset(self):
        """Resets the game by creating a new deck and clearing player hands"""
        self.deck = Deck(self.numDecks)
        self.deck.shuffle()
        for player in self.players:
            player.clear_hand()
        self.dealer.clear_hand()
        
    def deal_initial_cards(self):
        """Deals two initial cards to each player and the dealer."""
        for _ in range(2):
            for player in self.players:
                player.add_card(self.deck.deal_card())
            self.dealer.add_card(self.deck.deal_card())
            
    def play_round(self):
        """Plays a round of Blackjack."""
        self.deal_initial_cards()
        
        # Players take their turns
        for player in self.players:
            while player.hand_value() < 21:
                decision = player.make_decision(self.dealer.hand[0])
                if decision == PlayerAction.HIT:
                    player.add_card(self.deck.deal_card())
                else:
                    break
                    
        # Dealer's turn
        while self.dealer.hand_value() < 17:
            self.dealer.add_card(self.deck.deal_card())
            
        # Determine the outcome for each player
        for player in self.players:
            print(f"Player {player.name}'s hand: {player.hand} (Value: {player.hand_value()})")
            if player.hand_value() > 21:
                print(f"{player.name} busts!")
                player.process_loss()
            elif self.dealer.hand_value() > 21 or player.hand_value() > self.dealer.hand_value():
                print(f"{player.name} wins!")
                player.process_win()
            elif player.hand_value() == self.dealer.hand_value():
                pass
                print(f"{player.name} pushes (ties) with the dealer.")
            else:
                print(f"{player.name} loses.")
                player.process_loss()

        print(f"Dealer's hand: {self.dealer.hand} (Value: {self.dealer.hand_value()})")
        self.reset()
    