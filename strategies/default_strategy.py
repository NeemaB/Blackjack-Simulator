from enums import PlayerAction

class DefaultStrategy():

    def calc_player_action(self, dealer_up_card, player_hand_value, player_soft_aces):
        # Basic strategy logic can be implemented here
        # For simplicity, let's assume the player always hits if their hand value is less than 17
        if player_hand_value < 17:
            return PlayerAction.HIT
        else:
            return PlayerAction.STAND