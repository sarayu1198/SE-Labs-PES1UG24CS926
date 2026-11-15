import pytest
from bowling_alley import lane_cost, frame_score, lane_assignment


def test_lane_cost_weekday():
    assert lane_cost("weekday", 2, 4, 2, False) == 900


def test_lane_cost_weekend_large_group():
    assert lane_cost("weekend", 1, 5, 0, False) == 700


def test_lane_cost_league_discount():
    assert lane_cost("weekday", 2, 4, 2, True) == 720


def test_lane_cost_invalid_day():
    with pytest.raises(ValueError):
        lane_cost("holiday", 1, 2, 0, False)


def test_lane_cost_invalid_booking():
    with pytest.raises(ValueError):
        lane_cost("weekday", 0, 2, 0, False)


def test_lane_cost_too_many_shoes():
    with pytest.raises(ValueError):
        lane_cost("weekday", 1, 2, 3, False)


def test_frame_score_open_frame():
    assert frame_score(3, 4, []) == 7


def test_frame_score_spare():
    assert frame_score(5, 5, [3]) == 13


def test_frame_score_strike():
    assert frame_score(10, 2, [4, 5]) == 19


def test_frame_score_invalid_roll():
    with pytest.raises(ValueError):
        frame_score(-1, 0, [])


def test_frame_score_invalid_frame():
    with pytest.raises(ValueError):
        frame_score(7, 4, [])


def test_lane_assignment_wait():
    assert lane_assignment(2, False, 0) == "wait"


def test_lane_assignment_bumper():
    assert lane_assignment(2, True, 1) == "bumper lane"


def test_lane_assignment_two_lanes():
    assert lane_assignment(8, False, 2) == "two lanes"


def test_lane_assignment_standard():
    assert lane_assignment(4, False, 1) == "standard lane"
