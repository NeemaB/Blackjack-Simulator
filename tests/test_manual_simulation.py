from src.simulation.manual import ManualSimulation


class _DeckStub:
    def get_num_decks(self):
        return 1

    def get_shuffle_ratio(self):
        return 0.5

    def get_is_continuous_shuffle(self):
        return False


class _GameStub:
    def __init__(self, players, deck, isDebug=False):
        self.rounds_played = 0

    def play_round(self):
        self.rounds_played += 1


def test_manual_simulation_quits_after_first_round(monkeypatch, capsys):
    simulation = ManualSimulation(deck=_DeckStub(), players=[], isDebug=False)
    monkeypatch.setattr("src.simulation.manual.Game", _GameStub)
    monkeypatch.setattr("builtins.input", lambda _: "q")

    simulation.run_simulation()

    captured = capsys.readouterr()
    assert simulation.get_results()["totalGames"] == 1
    assert "Exiting manual simulation." in captured.out


def test_manual_simulation_runs_multiple_rounds(monkeypatch):
    simulation = ManualSimulation(deck=_DeckStub(), players=[], isDebug=False)
    inputs = iter(["", "q"])
    monkeypatch.setattr("src.simulation.manual.Game", _GameStub)
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    simulation.run_simulation()

    assert simulation.get_results()["totalGames"] == 2
