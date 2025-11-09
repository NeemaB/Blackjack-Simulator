# Test Suite

This directory contains all tests for the Blackjack Simulator.

## Running Tests

### Run all tests
```bash
python -m pytest tests/ -v
```

### Run specific test file
```bash
python -m pytest tests/test_continuous_shuffler.py -v
python -m pytest tests/test_reshuffle_policy.py -v
python -m pytest tests/strategies/test_chart_strategy.py -v
```

### Run with quiet output
```bash
python -m pytest tests/ -q
```

### Run with coverage
```bash
python -m pytest tests/ --cov
```

## Test Structure

```
tests/
├── test_continuous_shuffler.py  # Continuous shuffler tests (15 tests)
├── test_reshuffle_policy.py     # Traditional reshuffle tests (8 tests)
└── strategies/
    └── test_chart_strategy.py   # Strategy tests (2 tests)
```

## Test Files

### test_continuous_shuffler.py
Tests for continuous shuffle machine (CSM) functionality:
- `test_continuous_shuffler_resets_after_each_round` - Verifies all cards return after reset
- `test_traditional_shuffler_keeps_discards` - Verifies cards stay in discard pile
- `test_continuous_shuffler_multiple_rounds` - Tests multiple rounds
- `test_continuous_shuffler_with_heavy_usage` - Tests near-exhaustion scenarios

Uses parametrized tests with multiple deck counts (1, 2, 3, 4).

### test_reshuffle_policy.py
Tests for traditional shuffle ratio functionality:
- Verifies reshuffle behavior at various thresholds
- Tests with different deck counts and shuffle ratios
- Validates card composition after reshuffle

### strategies/test_chart_strategy.py
Tests for chart-based strategy decisions:
- Tests player action calculations
- Validates strategy against basic strategy chart

## Test Coverage

Total: 25 tests
- ✓ Continuous shuffler: 15 tests
- ✓ Traditional shuffler: 8 tests  
- ✓ Strategy logic: 2 tests

All tests passing.
