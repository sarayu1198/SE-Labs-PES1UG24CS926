# L6_L7_64 — Bowling Alley

## Lab 7: Fuzzing for Input Validation Bugs

### Files
- `bowling_alley_parser.py` — hardened parser functions.
- `test_bowling_alley_parser.py` — Hypothesis property-based no-crash tests.
- `SRN_NAME_LAB7.pdf` — add your four genuine terminal screenshots (SS1–SS4).

### Install dependencies
```bash
python3 -m pip install hypothesis pytest
```

### Run the application
```bash
python3 bowling_alley_parser.py
```

### Run the fuzz tests
```bash
python3 -m pytest -v test_bowling_alley_parser.py
```

### Fuzzing properties
Each test generates arbitrary Unicode text and `None` and verifies that its
corresponding function does not raise an exception.

### Defensive behavior for invalid inputs
- `format_player_name`: returns an empty string for non-string inputs.
- `parse_frame`: returns `(0, 0)` for malformed frames or non-string inputs.
- `parse_scoreboard`: skips malformed entries and returns `{}` for non-string inputs.

Valid notation and valid scoreboard entries retain their intended behavior.

### Screenshot evidence required
- SS1: run the original buggy `bowling_alley_parser.py`.
- SS2: run the completed Hypothesis tests against the original buggy module and show failures.
- SS3: run the fixed `bowling_alley_parser.py`.
- SS4: run the Hypothesis tests against the fixed module and show all tests passing.

Capture these screenshots from your own terminal after running the commands.
Do not use fabricated or reconstructed screenshots.
