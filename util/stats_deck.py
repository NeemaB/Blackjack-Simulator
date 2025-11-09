class StatsDeck:
    def __init__(self, deck=None):
        self.stats = { 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0 }
        self.total_cards = 0
        
        if deck is not None:
          cards = deck.get_available_cards()
          
          for card in cards:
            self.add_card(card.value())
            self.total_cards += 1
        
    def remove_card(self, card_value):
        if card_value in self.stats:
            self.stats[card_value] -= 1
            self.total_cards -= 1
            
    def add_card(self, card_value):
        if card_value in self.stats:
            self.stats[card_value] += 1
            self.total_cards += 1