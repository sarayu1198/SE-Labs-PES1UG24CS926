
from hypothesis import given, strategies as st

from bowling_alley_parser import (
    format_player_name,
    parse_frame,
    parse_scoreboard
)


@given(st.text() | st.none())
def test_format_player_name_no_crash(s):
    try:
        format_player_name(s)
    except Exception as e:
        assert False, f"format_player_name crashed with: {e}"


@given(st.text() | st.none())
def test_parse_frame_no_crash(s):
    try:
        parse_frame(s)
    except Exception as e:
        assert False, f"parse_frame crashed with: {e}"


@given(st.text() | st.none())
def test_parse_scoreboard_no_crash(s):
    try:
        parse_scoreboard(s)
    except Exception as e:
        assert False, f"parse_scoreboard crashed with: {e}"
