from enums import PlayerAction
from player import Player

class ChartStrategy:

    def __hard_total_action(self, dealer_up_card, player_hand_value):
        #TODO: Incorporate other player actions such as double down and split
        if player_hand_value >= 17:
            return PlayerAction.STAND
        
        if player_hand_value >= 13 and player_hand_value < 17:
            if dealer_up_card >= 7:
                return PlayerAction.HIT
            return PlayerAction.STAND
        
        if player_hand_value == 12:
            if dealer_up_card < 4:
                return PlayerAction.HIT
            elif dealer_up_card < 7:
                return PlayerAction.STAND
            else:
                return PlayerAction.HIT
        
        return PlayerAction.HIT

    def __soft_total_action(self, dealer_up_card, player_hand_value):
        #TODO: Incorporate other player actions such as double down and split
        if player_hand_value >= 19:
            return PlayerAction.STAND
        elif player_hand_value == 18:
            if dealer_up_card < 9:
                return PlayerAction.STAND
            return PlayerAction.HIT
        
        else:
            return PlayerAction.HIT

    def calc_player_action(self, dealer_up_card, player_hand_value, player_soft_aces):
        
        if player_soft_aces == 1:
            return self.__soft_total_action(dealer_up_card, player_hand_value)
        
        return self.__hard_total_action(dealer_up_card, player_hand_value)
        
        



    