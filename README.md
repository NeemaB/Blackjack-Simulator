# Blackjack Simulator

A simple python console application that allows a user to experiment with various blackjack setups and calculate the expected win/loss ratio of a player (or multiple) given a particular setup.

The `config.json` file can be updated to provide the following fields:

- numDecks: The number of decks the dealer is using
- shuffleRatio: The ratio of the original deck size, after which the shuffler will perform a reshuffle of the deck of cards
- players: The set of players to include in the game (the stats of each player will be displayed at the end)
- numGames: The number of rounds to play
- doubleDownEnabled: Whether the double down player action is enabled
- splitEnabled: Whether the split player action is enabled
- ddasEnabled: Whether the double down after split player action is enabled

Sample output after simulation ends:
```
Player: Alice, winnings: $-99650.0, total wins: 43123, total losses: 47749, total draws: 9128, win ratio: 0.43
Player: John, winnings: $-545500.0, total wins: 41047, total losses: 48566, total draws: 10387, win ratio: 0.41
Player: Timothy, winnings: $-78300.0, total wins: 43119, total losses: 47484, total draws: 9397, win ratio: 0.43
```


The *chart strategy* used is according to this table:
![BJA_Basic_Chart_Strategy](https://github.com/user-attachments/assets/798e5038-8aa2-452e-9c6d-c11d49f88aa1)


