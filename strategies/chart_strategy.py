from util import hand_util
from util.enums import PlayerAction
from player import Player

class ChartStrategy:
    """Represents a chart based strategy using a conventional blackjack strategy chart"""
    def __init__(self, splitEnabled=True, doubleDownEnabled=True, ddasEnabled=False):
        self.splitEnabled = splitEnabled, 
        self.doubleDownEnabled = doubleDownEnabled,
        self.ddasEnabled = ddasEnabled

    def __hard_total_action(
            self, 
            dealer_up_card, 
            player_hand):
        """Determine optimal player action when they have a hard total (no aces that are still counted as 11s) """
        
        player_hand_value = hand_util.hand_value(player_hand)

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

    def __soft_total_action(
            self, 
            dealer_up_card,  
            player_hand):
        """Determine optimal player action when they have a soft total (an ace that can still be converted to a 1)"""
        player_hand_value = hand_util.hand_value(player_hand)
         
        if player_hand_value >= 19:
            return PlayerAction.STAND
        elif player_hand_value == 18:
            if dealer_up_card < 9:
                return PlayerAction.STAND
            return PlayerAction.HIT
        
        else:
            return PlayerAction.HIT
        
    def __should_double_down(self, dealer_up_card, player_hand, is_soft_total, is_split):
        """Determine whether a player can/should double down based on strategy chart"""
        
        if not self.doubleDownEnabled:
            return False

        if len(player_hand) != 2:
            return False
            
        if is_split and not self.ddasEnabled:
            return False
        
        player_hand_value = hand_util.hand_value(player_hand)
        
        if is_soft_total:
            if player_hand_value == 19 and dealer_up_card == 6:
                return True
            elif player_hand_value == 18 and dealer_up_card < 7:
                return True
            elif player_hand_value == 17:
                if dealer_up_card > 2 and dealer_up_card < 7:
                    return True
            elif player_hand_value == 16 or player_hand == 15:
                if dealer_up_card > 3 and dealer_up_card < 7:
                    return True
            elif player_hand_value <= 14:
                if dealer_up_card == 5 or dealer_up_card == 6:
                    return True
            return False
            
        else:
            if player_hand_value == 11:
                return True
            elif player_hand_value == 10:
                if dealer_up_card < 10:
                    return True
            elif player_hand_value == 9:
                if dealer_up_card > 2 and dealer_up_card < 7:
                    return True
            return False
             
    def __should_split(self, dealer_up_card, player_hand):
        """Determine whether a player can/should split based on strategy chart"""
        if not self.splitEnabled:
            return False
        
        if len(player_hand) != 2:
            return False
        
        #TODO: Make allowing splits on different 10 valued cards configurable
        if player_hand[0].value != player_hand[1].value:
            return False
        split_value = player_hand[0].value
        
        if split_value == 11 or split_value == 8:
            return True
        
        if split_value == 9:
            if dealer_up_card < 7 or dealer_up_card == 8 or dealer_up_card == 9:
                return True
        
        if split_value == 7:
            if dealer_up_card < 8:
                return True
        
        if split_value == 6:
            if dealer_up_card == 2:
                if self.ddasEnabled:
                    return True
            elif dealer_up_card < 7:
                return True
        
        if split_value == 4:
            if dealer_up_card == 5 or dealer_up_card == 6:
                if self.ddasEnabled:
                    return True
        
        if split_value <= 3:
            if dealer_up_card < 4:
                if self.ddasEnabled:
                    return True
            elif dealer_up_card < 8:
                return True
                
        return False

    def calc_player_action(
            self, 
            dealer_up_card, 
            player_hand, 
            player_soft_aces, 
            is_split=False):
        
        if not is_split and self.__should_split(dealer_up_card, player_hand):
            return PlayerAction.SPLIT

        is_soft_total = player_soft_aces == 1
        
        if self.__should_double_down(dealer_up_card, player_hand, is_split, is_soft_total):
            return PlayerAction.DOUBLE_DOWN
        
        if is_soft_total:
            return self.__soft_total_action(dealer_up_card, player_hand)
        
        return self.__hard_total_action(dealer_up_card, player_hand)
        



    