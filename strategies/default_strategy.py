from util.enums import PlayerAction
from util import hand_util

class DefaultStrategy():

    def calc_player_action(
        self, 
        dealer_up_card, 
        player_hand, 
        player_soft_aces, 
        is_split=False):
        # Basic strategy logic can be implemented here
        # For simplicity, let's assume the player always hits if their hand value is less than 17
        if hand_util.hand_value(player_hand) < 17:
            return PlayerAction.HIT
        else:
            return PlayerAction.STAND