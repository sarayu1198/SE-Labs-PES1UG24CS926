
def format_player_name(name):
    """
    Title-cases a player name and cuts it to 10 characters.
    Returns an empty string for invalid input.
    """
    if not isinstance(name, str):
        return ""

    return name.strip().title()[:10]


def parse_frame(text):
    """
    Converts frame notation into pins knocked down:
    'X' -> (10, 0)
    '7/' -> (7, 3)
    '45' -> (4, 5)

    Returns (0, 0) for invalid input.
    """
    if not isinstance(text, str):
        return (0, 0)

    text = text.strip().upper()

    if text == 'X':
        return (10, 0)

    if len(text) != 2:
        return (0, 0)

    if not text[0].isdigit() or not text[0].isascii():
        return (0, 0)

    first = int(text[0])

    if text[1] == '/':
        return (first, 10 - first)

    if not text[1].isdigit() or not text[1].isascii():
        return (0, 0)

    second = int(text[1])

    if first + second > 10:
        return (0, 0)

    return (first, second)


def parse_scoreboard(text):
    """
    Parses 'Asha:150,Ravi:132' into a dictionary.
    Invalid entries are skipped instead of causing crashes.
    """
    scores = {}

    if not isinstance(text, str):
        return scores

    for entry in text.split(','):
        if ':' not in entry:
            continue

        name, score = entry.split(':', 1)

        name = name.strip()
        score = score.strip()

        if not name:
            continue

        try:
            scores[name] = int(score)
        except ValueError:
            continue

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
