"""Robust input parsers for a simple bowling-alley scoreboard."""


def format_player_name(name):
    """Title-case a player's name and limit it to 10 characters.

    Non-string or blank inputs produce an empty string.
    """
    if not isinstance(name, str):
        return ""
    return name.strip().title()[:10]


def parse_frame(text):
    """Parse one bowling frame into (first_roll, second_roll).

    Supported notation:
      X  -> (10, 0)
      7/ -> (7, 3)
      45 -> (4, 5)

    Invalid or unsupported input returns (0, 0).
    """
    if not isinstance(text, str):
        return 0, 0

    value = text.strip().upper()
    if value == "X":
        return 10, 0

    if len(value) != 2:
        return 0, 0

    first_char, second_char = value
    if first_char not in "0123456789":
        return 0, 0

    first = int(first_char)

    if second_char == "/":
        return first, 10 - first

    if second_char not in "0123456789":
        return 0, 0

    second = int(second_char)
    if first + second > 10:
        return 0, 0

    return first, second


def parse_scoreboard(text):
    """Parse comma-separated NAME:SCORE entries.

    Malformed entries are skipped. Non-string input produces an empty dict.
    """
    if not isinstance(text, str):
        return {}

    scores = {}
    for entry in text.split(","):
        if ":" not in entry:
            continue

        name, score_text = entry.split(":", 1)
        name = name.strip()
        score_text = score_text.strip()

        if not name or not score_text:
            continue

        try:
            score = int(score_text)
        except ValueError:
            continue

        if score < 0:
            continue

        scores[name] = score

    return scores


def main():
    print("==== Running format_player_name ====")
    value = input("Enter a player name for the scoreboard: ")
    print("Scoreboard name:", format_player_name(value))

    print("\n==== Running parse_frame ====")
    value = input("Enter a frame as X (strike), 7/ (spare) or two digits (e.g. 45): ")
    print("Pins (first roll, second roll):", parse_frame(value))

    print("\n==== Running parse_scoreboard ====")
    value = input("Enter scores as NAME:SCORE separated by commas (e.g. Asha:150,Ravi:132): ")
    print("Scoreboard:", parse_scoreboard(value))


if __name__ == "__main__":
    main()
