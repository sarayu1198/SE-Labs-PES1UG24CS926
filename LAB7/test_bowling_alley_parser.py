"""Hypothesis fuzz tests for the bowling alley input parser."""

from hypothesis import given, strategies as st

from bowling_alley_parser import (
    format_player_name,
    parse_frame,
    parse_scoreboard,
)


@given(st.text() | st.none())
def test_format_player_name_no_crash(value):
    try:
        format_player_name(value)
    except Exception as exc:
        assert False, f"format_player_name crashed with {value!r}: {exc}"


@given(st.text() | st.none())
def test_parse_frame_no_crash(value):
    try:
        parse_frame(value)
    except Exception as exc:
        assert False, f"parse_frame crashed with {value!r}: {exc}"


@given(st.text() | st.none())
def test_parse_scoreboard_no_crash(value):
    try:
        parse_scoreboard(value)
    except Exception as exc:
        assert False, f"parse_scoreboard crashed with {value!r}: {exc}"
